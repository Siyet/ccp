# coding: UTF-8
__author__ = 'cloud'

from django.db import models
from django.db.models import Q
from django.utils.text import ugettext_lazy as _
from django.conf import settings

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from smart_selects.db_fields import ChainedForeignKey
from model_utils import Choices

from dictionaries.models import FabricCategory

HARDNESS = Choices(('very_soft', _(u'Очень мягкий')),
                   ('soft', _(u'Мягкий')),
                   ('hard', _(u'Жесткий')),
                   ('very_hard', _(u'Очень жесткий')),
                   ('no_hardener', _(u'Без уплотнителя')))


class Collection(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    text = models.TextField(_(u'Описание'))
    image = models.ImageField(_(u'Изображение'))
    dickey = models.BooleanField(_(u'Манишка'))
    clasp = models.BooleanField(_(u'Застежка под штифты'))
    solid_yoke = models.BooleanField(_(u'Цельная кокетка'))
    shawl = models.BooleanField(_(u'Платок'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Коллекция')
        verbose_name_plural = _(u'Коллекции')

    def fabrics(self):
        filter_predicate = Q(residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL)
        filter_predicate &= Q(residuals__storehouse__collection=self.pk)
        return Fabric.objects.prefetch_related('residuals', 'residuals__storehouse').filter(filter_predicate)


class Storehouse(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    collection = models.ManyToManyField(Collection, verbose_name=_(u'Коллекция'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Склад')
        verbose_name_plural = _(u'Склады')


class FabricPrice(models.Model):
    storehouse = models.ForeignKey(Storehouse, verbose_name=_(u'Склад'), related_name='prices')
    fabric_category = models.ForeignKey('dictionaries.FabricCategory', verbose_name=_(u'Категория тканей'), related_name='prices')
    price = models.DecimalField(_(u'Цена'), max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.fabric_category.title

    class Meta:
        verbose_name = _(u'Цена ткани')
        verbose_name_plural = _(u'Цены тканей')


class Fabric(models.Model):
    code = models.CharField(_(u'Артикул'), max_length=20)
    category = models.ForeignKey('dictionaries.FabricCategory', verbose_name=_(u'Категория'), related_name='fabrics', blank=True, null=True)
    description = models.TextField(_(u'Описание'))
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


class FabricResidual(models.Model):
    storehouse = models.ForeignKey(Storehouse, verbose_name=_(u'Склад'), related_name='residuals')
    fabric = models.ForeignKey(Fabric, verbose_name=_(u'Ткань'), related_name='residuals')
    amount = models.DecimalField(_(u'Остаток'), max_digits=10, decimal_places=2)

    def __unicode__(self):
        return u'%s %s %s' % (self.fabric.code, _(u'на складе'), self.storehouse.title)

    class Meta:
        verbose_name = _(u'Остаток ткани')
        verbose_name_plural = _(u'Остатки тканей')
        unique_together = ('fabric', 'storehouse')


class Collar(models.Model):
    STAYS = Choices(('yes', _(u'Да')), ('no', _(u'Нет')), ('removable', _(u'Да, съемные')))
    stays = models.CharField(_(u'Косточки'), choices=STAYS, max_length=10)

    hardness = models.CharField(_(u'Жесткость'), choices=HARDNESS, max_length=15)

    type = models.ForeignKey('dictionaries.CollarType', verbose_name=_(u'Тип'))
    size = ChainedForeignKey('dictionaries.CollarButtons', chained_field='type', chained_model_field='types',
                             verbose_name=_(u'Пуговицы'), null=True)
    shirt = models.OneToOneField('backend.Shirt', related_name='collar')

    def __unicode__(self):
        return self.type.title

    class Meta:
        verbose_name = _(u'Воротник')
        verbose_name_plural = _(u'Воротники')


class Cuff(models.Model):
    hardness = models.CharField(_(u'Жесткость'), choices=HARDNESS, max_length=15)
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


class CustomButtons(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    picture = models.ImageField(_(u'Изображение'))
    type = models.ForeignKey('dictionaries.CustomButtonsType', verbose_name=_(u'Тип'))

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


class Dickey(models.Model):
    type = models.ForeignKey('dictionaries.DickeyType')
    fabric = models.ForeignKey(Fabric)

    def __unicode__(self):
        return self.type.title

    class Meta:
        verbose_name = _(u'Манишка')
        verbose_name_plural = _(u'Манишки')


class Initials(models.Model):
    FONTS = (('script', 'Script'), ('arial', 'Arial'), ('free', 'Free'))
    font = models.CharField(_(u'Шрифт'), choices=FONTS, max_length=10)

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

    is_template = models.BooleanField(_(u'Используется как шаблон'))
    code = models.CharField(_(u'Артикул'), max_length=255, null=True)
    material = models.CharField(_(u'Материал'), max_length=255)
    individualization = models.TextField(_(u'Индивидуализация'))
    description = models.TextField(_(u'Описание'))

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

    tuck = models.BooleanField(_(u'Вытачки'))

    back = models.ForeignKey('dictionaries.BackType', verbose_name=_(u'Спинка'), related_name='back_shirts')

    custom_buttons = models.ForeignKey(CustomButtons, verbose_name=_(u'Кастомные пуговицы'), null=True, blank=True)
    shawl = models.ForeignKey(ShawlOptions, verbose_name=_(u'Платок'))
    yoke = models.ForeignKey('dictionaries.YokeType', verbose_name=_(u'Кокетка'))
    clasp = models.BooleanField(_(u'Застежка под штифты'))

    STITCH = Choices(('none', _(u'0 мм (без отстрочки)')), ('1mm', _(u'1 мм (только съемные косточки)')), ('5mm', _(u'5 мм')))
    stitch = models.CharField(_(u'Ширина отстрочки'), max_length=10, choices=STITCH)

    dickey =  models.OneToOneField(Dickey, verbose_name=_(u'Манишка'), blank=True, null=True)
    initials = models.OneToOneField(Initials, verbose_name=_(u'Инициалы'), blank=True, null=True)


class CustomShirt(Shirt):

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
    shirt = models.ForeignKey(Shirt, verbose_name=_(u'Рубашка'))

    def __unicode__(self):
        return self.get_element_display()

    class Meta:
        verbose_name = _(u'Контрастная деталь')
        verbose_name_plural = _(u'Контрастные детали')
        unique_together = ['shirt', 'element']


class ContrastStitch(models.Model):
    ELEMENT = Choices(('shirt', _(u'Сорочка')),
                      ('cuffs', _(u'Манжеты')),
                      ('collar', _(u'Воротник')),
                      ('thread', _(u'Петель/ниток')))
    element = models.CharField(_(u'Элемент'), choices=ELEMENT, max_length=10)
    color = models.ForeignKey('dictionaries.StitchColor', verbose_name=_(u'Цвет отстрочки'))
    shirt = models.ForeignKey(Shirt)

    def __unicode__(self):
        return self.get_element_display()

    class Meta:
        verbose_name = _(u'Контрастная отстрочка')
        verbose_name_plural = _(u'Контрастные отстрочки')