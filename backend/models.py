# coding: UTF-8
import re

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.utils.text import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from smart_selects.db_fields import ChainedForeignKey
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel
from colorful.fields import RGBColorField

from dictionaries.models import FabricCategory, SleeveType, ResolveDefault
from backend import managers
from core import constants


class Collection(OrderedModel):
    storehouse = models.ForeignKey('backend.Storehouse', verbose_name=_(u'Склад'), related_name='collections',
                                   blank=False, null=True)
    title = models.CharField(_(u'Название'), max_length=255)
    filter_title = models.CharField(_(u'Наименование для фильтра'), max_length=255)
    about_shirt_title = models.CharField(_(u'Наименование для экрана "О сорочке"'), max_length=255)
    text = models.TextField(_(u'Описание'))
    image = models.ImageField(_(u'Изображение'), upload_to='collection')
    dickey = models.BooleanField(_(u'Манишка'))
    clasp = models.BooleanField(_(u'Застежка под штифты'))
    solid_yoke = models.BooleanField(_(u'Цельная кокетка'))
    shawl = models.BooleanField(_(u'Платок'))
    contrast_details = models.BooleanField(_(u'Контрастные детали'))
    white_fabric = models.ForeignKey('backend.Fabric', verbose_name=_(u'Ткань для опции "Воротник и манжеты полностью белые"'), null=True, blank=True)
    tuck = models.ManyToManyField('dictionaries.TuckType', verbose_name=_(u'Варианты вытачек'), related_name='collections')
    sex = models.CharField(_(u'Пол коллекции'), choices=constants.SEX, max_length=6, default=constants.SEX.male, blank=False)
    tailoring_time = models.CharField(_(u'Время пошива и доставки'), max_length=255, null=True)

    def __unicode__(self):
        return "%s %s" % (self.title, self.get_sex_display().lower())

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Коллекция')
        verbose_name_plural = _(u'Коллекции')

    def save(self, *args, **kwargs):
        if self.contrast_details:
            self.white_fabric = None
        return super(Collection, self).save(*args, **kwargs)

    def fabrics(self):
        filter_predicate = Q(residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL)
        filter_predicate &= Q(residuals__storehouse=self.storehouse.pk)
        return Fabric.objects.active.select_related('category', 'type', 'thickness') \
            .prefetch_related('residuals__storehouse', 'category__prices').filter(filter_predicate)


class Storehouse(models.Model):
    country = models.CharField(_(u'Страна'), max_length=255, unique=True)

    def __unicode__(self):
        return self.country

    class Meta:
        verbose_name = _(u'Склад')
        verbose_name_plural = _(u'Склады')


class Hardness(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255)
    collections = models.ManyToManyField(Collection, verbose_name=_(u'Коллекции'), related_name='hardness')

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Жесткость')
        verbose_name_plural = _(u'Жесткость')


class Stays(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255)
    collections = models.ManyToManyField(Collection, verbose_name=_(u'Коллекции'), related_name='stays')

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Косточки')
        verbose_name_plural = _(u'Косточки')


class Fit(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    collections = models.ManyToManyField(Collection, verbose_name=_(u'Коллекции'), related_name='fits')
    sizes = models.ManyToManyField('dictionaries.Size', verbose_name=_(u'Размеры'), related_name='fits')
    picture = models.ImageField(_(u'Изображение'), upload_to='fit')

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Тип талии')
        verbose_name_plural = _(u'Типы талии')

    def __unicode__(self):
        return self.title


class FabricPrice(TimeStampedModel):
    storehouse = models.ForeignKey(Storehouse, verbose_name=_(u'Склад'), related_name='prices')
    fabric_category = models.ForeignKey('dictionaries.FabricCategory', verbose_name=_(u'Категория тканей'),
                                        related_name='prices')
    price = models.DecimalField(_(u'Цена'), max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.fabric_category.title

    class Meta:
        verbose_name = _(u'Цена ткани')
        verbose_name_plural = _(u'Цены тканей')

    def get_shirts(self):
        return Shirt.objects.filter(fabric__category=self.fabric_category,
                                    collection__storehouse=self.storehouse).values('id')


class Fabric(TimeStampedModel):
    code = models.CharField(_(u'Артикул'), max_length=20, unique=True)
    category = models.ForeignKey('dictionaries.FabricCategory', verbose_name=_(u'Категория'), related_name='fabrics',
                                 blank=True, null=True)
    type = models.ForeignKey('dictionaries.FabricType', verbose_name=_(u'Тип'), related_name='fabrics',
                             null=True)
    thickness = models.ForeignKey('dictionaries.Thickness', verbose_name=_(u'Толщина'), related_name='fabrics',
                                  null=True)
    short_description = models.TextField(_(u'Краткое описание'), blank=True, default="")
    long_description = models.TextField(_(u'Полное описание'), blank=True, default="")
    material = models.CharField(_(u'Материал'), max_length=255, default="", blank=True)
    colors = models.ManyToManyField('dictionaries.FabricColor', verbose_name=_(u'Цвета'), related_name='color_fabrics')
    designs = models.ManyToManyField('dictionaries.FabricDesign', verbose_name=_(u'Дизайн'),
                                     related_name='design_fabrics')
    texture = models.OneToOneField('processing.Texture', verbose_name=_(u'Текстура'), related_name='fabric', null=True,
                                   on_delete=models.SET_NULL)
    dickey = models.BooleanField(_(u'Используется в манишке'), default=False)
    active = models.BooleanField(_(u'Активна'), default=True)

    objects = managers.FabricManager()

    def __unicode__(self):
        return self.code

    @property
    def get_sample(self):
        return self.texture.sample if self.texture else None

    def save(self, *args, **kwargs):
        category_letter = self.code[:1]

        if self.category and self.category.title != category_letter:
            try:
                category = FabricCategory.objects.get(title=category_letter)
                self.category = category
            except:
                pass

        super(Fabric, self).save(*args, **kwargs)

    @staticmethod
    def is_valid_code(code):
        return re.match(r'[A-Z]\d+$', code) if isinstance(code, basestring) else False

    class Meta(OrderedModel.Meta):
        ordering = ('code',)
        verbose_name = _(u'Ткань')
        verbose_name_plural = _(u'Ткани')


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

    objects = managers.TypedManager()

    def __unicode__(self):
        return unicode(self.type)

    class Meta:
        verbose_name = _(u'Воротник')
        verbose_name_plural = _(u'Воротники')


class Cuff(models.Model):
    hardness = models.ForeignKey(Hardness, verbose_name=_(u'Жесткость'), null=True)
    type = models.ForeignKey('dictionaries.CuffType', verbose_name=_(u'Тип'), related_name='type_cuffs')
    rounding = ChainedForeignKey('dictionaries.CuffRounding', verbose_name=_(u'Тип закругления'), chained_field='type',
                                 chained_model_field='types', show_all=False, null=True, blank=True)

    shirt = models.OneToOneField('backend.Shirt', related_name='cuff')

    objects = managers.TypedManager()

    def __unicode__(self):
        return unicode(self.type)

    def save(self, *args, **kwargs):
        if not self.shirt.sleeve.cuffs:
            if self.id:
                self.delete()
            return None

        return super(Cuff, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'Манжета')
        verbose_name_plural = _(u'Манжеты')


class CustomButtons(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255)
    picture = models.ImageField(_(u'Изображение'), upload_to='custombuttons')
    type = models.ForeignKey('dictionaries.CustomButtonsType', verbose_name=_(u'Тип'), related_name='buttons')
    color = RGBColorField(_(u'Цвет'), default="#FFFFFF")

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Кастомные пуговицы')
        verbose_name_plural = _(u'Кастомные пуговицы')


class ShawlOptions(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255)
    extra_price = models.DecimalField(_(u'Добавочная стоимость'), max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Настройки платка')
        verbose_name_plural = _(u'Настройки платка')

    def get_shirts(self):
        return Shirt.objects.filter(shawl=self).values('id')


class Dickey(models.Model):
    type = models.ForeignKey('dictionaries.DickeyType', verbose_name=_(u'Тип'))
    fabric = models.ForeignKey(Fabric, verbose_name=_(u'Ткань'), related_name='dickey_list',
                               limit_choices_to={'dickey': True})
    shirt = models.OneToOneField('backend.Shirt', related_name='dickey')

    objects = managers.TypedManager()

    def __unicode__(self):
        return unicode(self.type)

    class Meta:
        verbose_name = _(u'Манишка')
        verbose_name_plural = _(u'Манишки')

    def get_shirts(self):
        return [self.shirt]


class Initials(models.Model):
    font = models.ForeignKey('dictionaries.Font', verbose_name=_(u'Шрифт'), null=True)
    shirt = models.OneToOneField('backend.Shirt', related_name='initials')

    LOCATION = Choices(
        ('button2', _(u'2 пуговица')),
        ('button3', _(u'3 пуговица')),
        ('button4', _(u'4 пуговица')),
        ('button5', _(u'5 пуговица')),
        ('hem', _(u'Низ (л)')),
        ('pocket', _(u'Карман (л)')),
        ('cuff', _(u'Манжета (л)'))
    )
    location = models.CharField(_(u'Местоположение'), choices=LOCATION, max_length=10)
    text = models.CharField(_(u'Текст'), max_length=255)
    color = models.ForeignKey('dictionaries.Color', verbose_name=_(u'Цвет'))

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = _(u'Инициалы')
        verbose_name_plural = _(u'Инициалы')


class Shirt(models.Model):
    related_fields = ["collection", "fabric", "size_option", "size", "hem", "placket", "pocket", "back",
                      "custom_buttons_type", "custom_buttons", "shawl", "yoke"]

    CLASP_OPTIONS = Choices((False, _(u'Не использовать застежку')), (True, _(u'Использовать застежку')))

    is_template = models.BooleanField(_(u'Используется как шаблон'), default=False)
    is_standard = models.BooleanField(_(u'Используется как стандартный вариант'), default=False, editable=False)
    collection = models.ForeignKey(Collection, verbose_name=_(u'Коллекция'), related_name='shirts', null=True)
    code = models.CharField(_(u'Артикул'), max_length=255, null=True)
    individualization = models.TextField(_(u'Индивидуализация'), null=True, blank=True)

    fabric = models.ForeignKey(Fabric, verbose_name=_(u'Ткань'), null=True)

    showcase_image = models.ImageField(_(u'Изображение для витрины'), blank=False, null=True, upload_to='showcase')
    showcase_image_list = ImageSpecField(source='showcase_image',
                                         processors=[ResizeToFill(*settings.SHOWCASE_IMAGE_SIZE)],
                                         format='JPEG',
                                         options={'quality': 100})

    showcase_image_detail = ImageSpecField(source='showcase_image',
                                           processors=[ResizeToFill(*settings.SHOWCASE_DETAILS_IMAGE_SIZE)],
                                           format='JPEG',
                                           options={'quality': 100})

    size_option = models.ForeignKey('dictionaries.SizeOptions', verbose_name=_(u'Выбранный вариант размера'))
    size = models.ForeignKey('dictionaries.Size', verbose_name=_(u'Размер'), blank=True, null=True)

    hem = models.ForeignKey('dictionaries.HemType', verbose_name=_(u'Низ'), related_name='hem_shirts')
    placket = models.ForeignKey('dictionaries.PlacketType', verbose_name=_(u'Полочка'), related_name='placket_shirts')
    pocket = models.ForeignKey('dictionaries.PocketType', verbose_name=_(u'Карман'), related_name='pocket_shirts')
    sleeve = models.ForeignKey('dictionaries.SleeveType', verbose_name=_(u'Рукав'), related_name='sleeve_shirts',
                               default=ResolveDefault(SleeveType))
    fit = models.ForeignKey(Fit, verbose_name=_(u'Талия'), blank=True, null=True)
    # fit = models.ForeignKey('dictionaries.Fit', verbose_name=_(u'Талия'), blank=True, null=True)
    sleeve_length = models.ForeignKey('dictionaries.SleeveLength', verbose_name=_(u'Длина рукава'), blank=True, null=True)

    tuck = ChainedForeignKey('dictionaries.TuckType', verbose_name=_(u'Вытачки'), chained_field='collection',
                             chained_model_field='collections', show_all=False)

    back = models.ForeignKey('dictionaries.BackType', verbose_name=_(u'Спинка'), related_name='back_shirts')

    custom_buttons_type = models.ForeignKey('dictionaries.CustomButtonsType', verbose_name=_(u'Тип кастомных пуговиц'),
                                            null=True, blank=True, related_name='back_shirts')
    custom_buttons = ChainedForeignKey(CustomButtons, verbose_name=_(u'Кастомные пуговицы'),
                                       chained_field='custom_buttons_type',
                                       chained_model_field='type', show_all=False, null=True, blank=True)

    shawl = models.ForeignKey(ShawlOptions, verbose_name=_(u'Платок'), null=True, default=ResolveDefault(ShawlOptions))
    yoke = models.ForeignKey('dictionaries.YokeType', verbose_name=_(u'Кокетка'), null=True)
    clasp = models.BooleanField(_(u'Застежка под штифты'), choices=CLASP_OPTIONS, default=False)

    STITCH = Choices(('none', _(u'0 мм (без отстрочки)')), ('1mm', _(u'1 мм (только съемные косточки)')),
                     ('5mm', _(u'5 мм')))
    stitch = models.CharField(_(u'Ширина отстрочки'), max_length=10, choices=STITCH)

    price = models.DecimalField(_(u'Цена'), max_digits=10, decimal_places=2, editable=False, null=True)


    def save(self, *args, **kwargs):
        cuff = getattr(self, 'cuff', None)
        if cuff and not self.sleeve.cuffs:
            if cuff.id:
                cuff.delete()

        super(Shirt, self).save(*args, **kwargs)

    class Meta:
        ordering = ('code',)
        verbose_name = _(u'Рубашка')
        verbose_name_plural = _(u'Рубашки')

    def __unicode__(self):
        return self.code if self.code else self.id


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
        return u"%s #%s" % (_(u"Рубашка"), self.id)


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
        return u"%s #%s" % (_(u"Шаблон"), self.code)


class StandardShirt(Shirt):
    objects = managers.StandardShirtManager()

    class Meta:
        proxy = True
        verbose_name = _(u'Стандартный вариант рубашки')
        verbose_name_plural = _(u'Стандартные варианты рубашек')

    def __unicode__(self):
        return u"%s #%s" % (_(u"Стандартный вариант"), self.code)

    def save(self, *args, **kwargs):
        self.is_template = False
        self.is_standard = True
        super(StandardShirt, self).save(*args, **kwargs)

    def validate_unique(self, exclude=None):
        super(StandardShirt, self).validate_unique(exclude)
        if self.collection:
            qs = StandardShirt.objects.filter(collection=self.collection)
            if self.pk is not None:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError([_(u'Стандартный вариант для коллекции уже существует')])


class ShirtImage(models.Model):
    image = models.ImageField(_(u'Изображение'), upload_to='showcase')
    shirt = models.ForeignKey(Shirt, related_name='shirt_images')

    class Meta:
        verbose_name = _(u'Изображение')
        verbose_name_plural = _(u'Изображения')


class ContrastDetails(models.Model):
    COLLAR_ELEMENTS = Choices(
        ('collar_face', _(u'Воротник лицевая сторона')),
        ('collar_bottom', _(u'Воротник низ')),
        ('collar_outer', _(u'Воротник внешняя стойка')),
        ('collar_inner', _(u'Воротник внутрення стойка'))
    )
    CUFF_ELEMENTS = Choices(
        ('cuff_outer', _(u'Манжета внешняя')),
        ('cuff_inner', _(u'Манжета внутрення'))
    )
    ELEMENTS = COLLAR_ELEMENTS + CUFF_ELEMENTS
    element = models.CharField(_(u'Элемент'), choices=ELEMENTS, max_length=20)
    fabric = models.ForeignKey(Fabric, verbose_name=_(u'Ткань'))
    shirt = models.ForeignKey(Shirt, verbose_name=_(u'Рубашка'), related_name='contrast_details')

    def __unicode__(self):
        return self.get_element_display()

    class Meta:
        verbose_name = _(u'Контрастная деталь')
        verbose_name_plural = _(u'Контрастные детали')
        unique_together = ['shirt', 'element']

    def get_shirts(pk=None, exclude=None):
        qs = Shirt.objects.filter(contrast_details__isnull=False)
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
    shirt = models.ForeignKey(Shirt, related_name='contrast_stitches')

    def __unicode__(self):
        return u""

    class Meta:
        verbose_name = _(u'Контрастная отстрочка')
        verbose_name_plural = _(u'Контрастные отстрочки')


class AccessoriesPrice(models.Model):
    content_type_names = {
        _(u'Контрастная деталь'): _(u'Контрастные ткани'),
    }

    content_type = models.OneToOneField(ContentType, verbose_name=_('content type'), related_name='accessories_price',
                                        limit_choices_to={'model__in': ('dickey', 'contrastdetails')})
    price = models.DecimalField(_(u'Цена'), max_digits=10, decimal_places=2)

    def __unicode__(self):
        return _(u'Цена: %s') % self.content_type

    def content_type_title(self):
        return self.content_type_names.get(self.content_type.name, self.content_type.name)

    content_type_title.allow_tags = True
    content_type_title.short_description = _(u'Тип')

    class Meta:
        verbose_name = _(u'Цена надбавки')
        verbose_name_plural = _(u'Цены надбавок')
