# coding: UTF-8
from django.contrib.contenttypes.fields import GenericForeignKey

__author__ = 'cloud'

from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.utils.text import ugettext_lazy as _
from django.conf import settings

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from smart_selects.db_fields import ChainedForeignKey
from model_utils import Choices

from dictionaries.models import FabricCategory
from backend import managers


SEX = Choices(
    ('male', _(u'Мужской')),
    ('female', _(u'Женский')),
    ('unisex', _(u'Унисекс')),
)


class Collection(models.Model):
    storehouse = models.ForeignKey('backend.Storehouse', verbose_name=_(u'Склад'), related_name='collections', blank=False, null=True)
    title = models.CharField(_(u'Название'), max_length=255)
    text = models.TextField(_(u'Описание'))
    image = models.ImageField(_(u'Изображение'))
    dickey = models.BooleanField(_(u'Манишка'))
    clasp = models.BooleanField(_(u'Застежка под штифты'))
    solid_yoke = models.BooleanField(_(u'Цельная кокетка'))
    shawl = models.BooleanField(_(u'Платок'))
    sex = models.CharField(_(u'Пол'), choices=SEX, max_length=6, default='male', blank=False)
    tailoring_time = models.CharField(_(u'Время пошива и доставки'), max_length=255, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Коллекция')
        verbose_name_plural = _(u'Коллекции')

    def fabrics(self):
        filter_predicate = Q(residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL)
        filter_predicate &= Q(residuals__storehouse=self.storehouse.pk)
        return Fabric.objects.select_related('fabric_type').prefetch_related('residuals__storehouse').filter(filter_predicate)


class Storehouse(models.Model):
    country = models.CharField(_(u'Страна'), max_length=255, unique=True)

    def __unicode__(self):
        return self.country

    class Meta:
        verbose_name = _(u'Склад')
        verbose_name_plural = _(u'Склады')


class Hardness(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    collections = models.ManyToManyField(Collection, verbose_name=_(u'Коллекции'), related_name='hardness')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Жесткость')
        verbose_name_plural = _(u'Жесткость')


class Stays(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    collections = models.ManyToManyField(Collection, verbose_name=_(u'Коллекции'), related_name='stays')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Косточки')
        verbose_name_plural = _(u'Косточки')


class FabricPrice(models.Model):
    storehouse = models.ForeignKey(Storehouse, verbose_name=_(u'Склад'), related_name='prices')
    fabric_category = models.ForeignKey('dictionaries.FabricCategory', verbose_name=_(u'Категория тканей'), related_name='prices')
    price = models.DecimalField(_(u'Цена'), max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.fabric_category.title

    class Meta:
        verbose_name = _(u'Цена ткани')
        verbose_name_plural = _(u'Цены тканей')

    def get_shirts(self):
        return Shirt.objects.filter(fabric__category=self.fabric_category, collection__storehouse=self.storehouse).values('id')


class Fabric(models.Model):
    code = models.CharField(_(u'Артикул'), max_length=20, unique=True)
    category = models.ForeignKey('dictionaries.FabricCategory', verbose_name=_(u'Категория'), related_name='fabrics', blank=True, null=True)
    fabric_type = models.ForeignKey('dictionaries.FabricType', verbose_name=_(u'Тип'), related_name='fabrics', null=True)
    description = models.TextField(_(u'Описание'), null=True)
    material = models.CharField(_(u'Материал'), max_length=255, null=True)
    colors = models.ManyToManyField('dictionaries.FabricColor', verbose_name=_(u'Цвета'), related_name='color_fabrics')
    designs = models.ManyToManyField('dictionaries.FabricDesign', verbose_name=_(u'Дизайн'), related_name='design_fabrics')
    texture = models.ImageField(_(u'Текстура'))

    def __unicode__(self):
        return self.code

    def save(self, *args, **kwargs):
        category_letter = self.code[0]
        try:
            category = FabricCategory.objects.get(title=category_letter)
            self.category = category
        except:
            pass

        super(Fabric, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'Ткань')
        verbose_name_plural = _(u'Ткани')
        ordering = ('code', )


class FabricResidual(models.Model):
    storehouse = models.ForeignKey(Storehouse, verbose_name=_(u'Склад'), related_name='residuals')
    fabric = models.ForeignKey(Fabric, verbose_name=_(u'Ткань'), related_name='residuals')
    amount = models.DecimalField(_(u'Остаток'), max_digits=10, decimal_places=2, default=0)

    def __unicode__(self):
        return u'%s %s %s' % (self.fabric.code, _(u'на складе'), self.storehouse)

    class Meta:
        verbose_name = _(u'Остаток ткани')
        verbose_name_plural = _(u'Остатки тканей')
        unique_together = ('fabric', 'storehouse')


class Collar(models.Model):
    stays = models.ForeignKey(Stays, verbose_name=_(u'Косточки'), null=True)
    hardness = models.ForeignKey(Hardness, verbose_name=_(u'Жесткость'), null=True)

    type = models.ForeignKey('dictionaries.CollarType', verbose_name=_(u'Тип'))
    size = ChainedForeignKey('dictionaries.CollarButtons', chained_field='type', chained_model_field='types',
                             verbose_name=_(u'Пуговицы'), null=True)
    shirt = models.OneToOneField('backend.Shirt', related_name='collar')

    def __unicode__(self):
        return self.type.title

    class Meta:
        verbose_name = _(u'Воротник')
        verbose_name_plural = _(u'Воротники')

    @staticmethod
    def get_related_shirts(pk=None, exclude=None):
        qs = Shirt.objects.filter(collar__isnull=False)
        if pk:
            qs = qs.filter(collar__id=pk)
        if exclude:
            qs = qs.exclude(collar__id__in=exclude)
        return qs.values('id').distinct()


class Cuff(models.Model):
    hardness = models.ForeignKey(Hardness, verbose_name=_(u'Жесткость'), null=True)
    sleeve = models.ForeignKey('dictionaries.SleeveType', verbose_name=_(u'Рукав'), related_name='sleeve_cuff')

    type = models.ForeignKey('dictionaries.CuffType', verbose_name=_(u'Тип'), related_name='cuff')
    rounding = ChainedForeignKey('dictionaries.CuffRounding', verbose_name=_(u'Тип закругления'), chained_field='type',
                                 chained_model_field='types', show_all=False, null=True)

    shirt = models.OneToOneField('backend.Shirt', related_name='shirt_cuff')

    def __unicode__(self):
        return self.type.title

    class Meta:
        verbose_name = _(u'Манжета')
        verbose_name_plural = _(u'Манжеты')

    @staticmethod
    def get_related_shirts(pk=None, exclude=None):
        qs = Shirt.objects.filter(shirt_cuff__isnull=False)
        if pk:
            qs = qs.filter(shirt_cuff__id=pk)
        if exclude:
            qs = qs.exclude(shirt_cuff__id__in=exclude)
        return qs.values('id').distinct()


class CustomButtons(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    picture = models.ImageField(_(u'Изображение'))
    type = models.ForeignKey('dictionaries.CustomButtonsType', verbose_name=_(u'Тип'), related_name='buttons')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Кастомные пуговицы')
        verbose_name_plural = _(u'Кастомные пуговицы')


class ShawlOptions(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    extra_price = models.DecimalField(_(u'Добавочная стоимость'), max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Настройки платка')
        verbose_name_plural = _(u'Настройки платка')

    def get_shirts(self):
        return Shirt.objects.filter(shawl=self).values('id')


class Dickey(models.Model):
    type = models.ForeignKey('dictionaries.DickeyType')
    fabric = models.ForeignKey(Fabric)

    def __unicode__(self):
        return self.type.title

    class Meta:
        verbose_name = _(u'Манишка')
        verbose_name_plural = _(u'Манишки')

    @staticmethod
    def get_related_shirts(pk=None, exclude=None):
        qs = Shirt.objects.filter(dickey__isnull=False)
        if pk:
            qs = qs.filter(dickey__id=pk)
        if exclude:
            qs = qs.exclude(dickey__id__in=exclude)
        return qs.values('id').distinct()


class Initials(models.Model):
    font = models.ForeignKey('dictionaries.Font', verbose_name=_(u'Шрифт'), null=True)

    LOCATION = (('button2', _(u'2 пуговица')),
                ('button3', _(u'3 пуговица')),
                ('button4', _(u'4 пуговица')),
                ('button5', _(u'5 пуговица')),
                ('hem', _(u'Низ (л)')),
                ('pocket', _(u'Карман (л)')),
                ('cuff', _(u'Манжета (л)')))
    location = models.CharField(_(u'Местоположение'), choices=LOCATION, max_length=10)
    text = models.CharField(_(u'Текст'), max_length=255)
    color = models.ForeignKey('dictionaries.Color', verbose_name=_(u'Цвет'))

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = _(u'Инициалы')
        verbose_name_plural = _(u'Инициалы')


class Shirt(models.Model):
    TUCK_OPTIONS = Choices((False, _(u'Без вытачек')), (True, _(u'С вытачками')))
    CLASP_OPTIONS = Choices((False, _(u'Не использовать застежку')), (True, _(u'Использовать застежку')))

    is_template = models.BooleanField(_(u'Используется как шаблон'))
    collection = models.ForeignKey(Collection, verbose_name=_(u'Коллекция'), related_name='shirts', blank=False, null=True)
    code = models.CharField(_(u'Артикул'), max_length=255, null=True)
    individualization = models.TextField(_(u'Индивидуализация'))
    description = models.TextField(_(u'Описание'), blank=True, null=True)

    fabric = models.ForeignKey(Fabric, verbose_name=_(u'Ткань'))

    showcase_image = models.ImageField(_(u'Изображение для витрины'), blank=False, null=True, upload_to='showcase')
    showcase_image_list = ImageSpecField(source='showcase_image',
                                      processors=[ResizeToFill(200, 300)],
                                       format='JPEG',
                                      options={'quality': 80})

    showcase_image_detail = ImageSpecField(source='showcase_image',
                                      processors=[ResizeToFill(400, 600)],
                                      format='JPEG',
                                      options={'quality': 80})

    size_option = models.ForeignKey('dictionaries.SizeOptions', verbose_name=_(u'Выбранный вариант размера'))
    size = models.ForeignKey('dictionaries.Size', verbose_name=_(u'Размер'), blank=True, null=True)

    hem = models.ForeignKey('dictionaries.HemType', verbose_name=_(u'Низ'), related_name='hem_shirts')
    placket = models.ForeignKey('dictionaries.PlacketType', verbose_name=_(u'Полочка'), related_name='placket_shirts')
    pocket = models.ForeignKey('dictionaries.PocketType', verbose_name=_(u'Карман'), related_name='pocket_shirts')

    tuck = models.BooleanField(verbose_name=_(u'Вытачки'), choices=TUCK_OPTIONS, default=False)

    back = models.ForeignKey('dictionaries.BackType', verbose_name=_(u'Спинка'), related_name='back_shirts')

    custom_buttons_type = models.ForeignKey('dictionaries.CustomButtonsType', verbose_name=_(u'Тип кастомных пуговиц'), null=True, blank=True, related_name='back_shirts')
    custom_buttons = ChainedForeignKey(CustomButtons, verbose_name=_(u'Кастомные пуговицы'), chained_field='custom_buttons_type',
                                 chained_model_field='type', show_all=False, null=True, blank=True)

    shawl = models.ForeignKey(ShawlOptions, verbose_name=_(u'Платок'))
    yoke = models.ForeignKey('dictionaries.YokeType', verbose_name=_(u'Кокетка'))
    clasp = models.BooleanField(_(u'Застежка под штифты'), choices=CLASP_OPTIONS, default=False)

    STITCH = Choices(('none', _(u'0 мм (без отстрочки)')), ('1mm', _(u'1 мм (только съемные косточки)')), ('5mm', _(u'5 мм')))
    stitch = models.CharField(_(u'Ширина отстрочки'), max_length=10, choices=STITCH)

    dickey = models.OneToOneField(Dickey, verbose_name=_(u'Манишка'), blank=True, null=True)
    initials = models.OneToOneField(Initials, verbose_name=_(u'Инициалы'), blank=True, null=True)
    price = models.DecimalField(_(u'Цена'), max_digits=10, decimal_places=2, editable=False, null=True)

    def calculate_price(self):
        price = 0

        # Платок
        try:
            shawl_price = self.shawl.extra_price
        except AttributeError:
            shawl_price = 0
        price += shawl_price

        # Кастомные пуговицы
        try:
            custom_buttons_price = self.custom_buttons.type.extra_price
        except AttributeError:
            custom_buttons_price = 0
        price += custom_buttons_price

        # Манишка
        dickey_price = AccessoriesPrice.objects.filter(content_type__app_label='backend', content_type__model='dickey').filter(Q(object_pk__isnull=True) | Q(object_pk=self.shawl_id)).order_by('-object_pk').first()
        if dickey_price and self.dickey:
            price += dickey_price.price

        # Контрастные детали
        contrast_detail_price = AccessoriesPrice.objects.filter(content_type__app_label='backend', content_type__model='contrastdetails').first()
        # Не зависимо от количества
        if contrast_detail_price and self.shirt_contrast_details.count() > 0:
            price += contrast_detail_price.price

        # Воротник или манжета. Наличие хотя бы одного прибавляем цену
        if hasattr(self, 'shirt_cuff') or hasattr(self, 'collar'):
            cuff_price = AccessoriesPrice.objects.filter(Q(content_type__app_label='backend') & (Q(content_type__model='cuff') | Q(content_type__model='collar'))).order_by('-object_pk').first()
            if cuff_price:
                price += cuff_price.price

        try:
            fabric_prices = (x for x in self.collection.storehouse.prices.all() if x.fabric_category_id == self.fabric.category_id)
            return price + next(fabric_prices).price
        except StopIteration:
            return price
        except AttributeError:
            return price

    def save(self, *args, **kwargs):
        self.price = self.calculate_price()
        super(Shirt, self).save(*args, **kwargs)


class CustomShirt(Shirt):
    objects = managers.CustomShirtManager()

    def save(self, *args, **kwargs):
        self.is_template = False
        super(CustomShirt, self).save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = _(u'Рубашка')
        verbose_name_plural = _(u'Рубашки')

    def __unicode__(self):
        return u"%s #%s" %(_(u"Рубашка"), self.id)


class TemplateShirt(Shirt):
    objects = managers.TemplateShirtManager()

    def save(self, *args, **kwargs):
        self.is_template = True
        super(TemplateShirt, self).save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = _(u'Шаблон рубашки')
        verbose_name_plural = _(u'Шаблоны рубашек')

    def __unicode__(self):
        return u"%s #%s" %(_(u"Шаблон"), self.code)


class ShirtImage(models.Model):
    image = models.ImageField(_(u'Изображение'), upload_to='showcase')
    shirt = models.ForeignKey(Shirt, related_name='shirt_images')

    class Meta:
        verbose_name = _(u'Изображение')
        verbose_name_plural = _(u'Изображения')


class ContrastDetails(models.Model):
    ELEMENTS = (('collar_face', _(u'Воротник лицевая сторона')),
                ('collar_bottom', _(u'Воротник низ')),
                ('collar_outer', _(u'Воротник внешняя стойка')),
                ('collar_inner', _(u'Воротник внутрення стойка')),
                ('cuff_outer', _(u'Манжета внешняя')),
                ('cuff_inner', _(u'Манжета внутрення')))
    element = models.CharField(_(u'Элемент'), choices=ELEMENTS, max_length=20)
    fabric = models.ForeignKey(Fabric, verbose_name=_(u'Ткань'))
    shirt = models.ForeignKey(Shirt, verbose_name=_(u'Рубашка'), related_name='shirt_contrast_details')

    def __unicode__(self):
        return self.get_element_display()

    class Meta:
        verbose_name = _(u'Контрастная деталь')
        verbose_name_plural = _(u'Контрастные детали')
        unique_together = ['shirt', 'element']

    @staticmethod
    def get_related_shirts(pk=None, exclude=None):
        qs = Shirt.objects.filter(shirt_contrast_details__isnull=False)
        return qs.values('id').distinct()


class ElementStitch(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    collections = models.ManyToManyField(Collection, verbose_name=_(u'Коллекции'), related_name='stitches')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Отстрочка')
        verbose_name_plural = _(u'Отстрочки')


class ContrastStitch(models.Model):
    element = models.ForeignKey(ElementStitch, verbose_name=u'Элемент', null=True)
    color = models.ForeignKey('dictionaries.StitchColor', verbose_name=_(u'Цвет отстрочки'))
    shirt = models.ForeignKey(Shirt)

    def __unicode__(self):
        return self.element.title

    class Meta:
        verbose_name = _(u'Контрастная отстрочка')
        verbose_name_plural = _(u'Контрастные отстрочки')


class AccessoriesPrice(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name='accessories_price')
    object_pk = models.IntegerField(_('object ID'), blank=True, null=True)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    price = models.DecimalField(_(u'Цена'), max_digits=10, decimal_places=2)
    collections = models.ManyToManyField(Collection, verbose_name=_(u'Коллекции'), related_name='accessories_prices', blank=True)

    def __unicode__(self):
        return u'Цена: %s' % self.content_type

    class Meta:
        verbose_name = _(u'Цена надбавки')
        verbose_name_plural = _(u'Цены надбавок')
        unique_together = [('content_type', 'object_pk', )]

    def get_content_object(self):
        try:
            return self.content_object
        except ValueError:
            return None

    def get_shirts(self):
        if self.object_pk:
            return self.content_type.model_class().get_related_shirts(pk=self.object_pk)
        else:
            return self.content_type.model_class().get_related_shirts(exclude=AccessoriesPrice.objects.filter(content_type=self.content_type, object_pk__isnull=False).values('object_pk'))
