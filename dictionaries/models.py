# coding: utf-8

from django.db import models
from django.utils.text import ugettext_lazy as _
from colorful.fields import RGBColorField
from django.db.models import Count


class ComponentModel(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    picture = models.ImageField(_(u'Изображение'))

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class Color(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, default=u'')
    color = RGBColorField(_(u'Значение'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Цвет (для инициалов)'
        verbose_name_plural = u'Цвета (для инициалов)'


class Font(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    font = models.FileField(_(u'Файл шрифта'), upload_to='fonts')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Шрифт (для инициалов)'
        verbose_name_plural = u'Шрифты (для инициалов)'


class FabricColor(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    value = RGBColorField(_(u'Значение'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Цвет ткани')
        verbose_name_plural = _(u'Цвета тканей')

    @staticmethod
    def used():
        return FabricColor.objects.prefetch_related('color_fabrics').annotate(fabrics_count=Count('color_fabrics')).filter(fabrics_count__gt=0)


class FabricCategory(models.Model):
    title = models.CharField(_(u'Категория'), unique=True, max_length=1, db_index=True)

    def __unicode__(self):
        return u"%s %s" % (_(u'Категория'), self.title)

    class Meta:
        verbose_name = _(u'Категория ткани')
        verbose_name_plural = _(u'Категории тканей')


class FabricType(models.Model):
    title = models.CharField(_(u'Тип'), unique=True, max_length=255)

    def __unicode__(self):
        return u"%s %s" % (_(u'Тип'), self.title)

    class Meta:
        verbose_name = _(u'Тип ткани')
        verbose_name_plural = _(u'Типы тканей')


class FabricDesign(ComponentModel):
    class Meta:
        verbose_name = _(u'Паттерн ткани')
        verbose_name_plural = _(u'Паттерны тканей')

    @staticmethod
    def used():
        return FabricDesign.objects.prefetch_related('design_fabrics').annotate(fabrics_count=Count('design_fabrics')).filter(fabrics_count__gt=0)


class CollarType(ComponentModel):
    buttons = models.ManyToManyField('CollarButtons', verbose_name=_(u'Варианты пуговиц'))

    class Meta:
        verbose_name = _(u'Тип воротника')
        verbose_name_plural = _(u'Типы воротников')


class CollarButtons(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    types = models.ManyToManyField('CollarType', verbose_name=_(u'Типы воротников'), through=CollarType.buttons.through,
                                   blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Пуговицы воротника')
        verbose_name_plural = _(u'Пуговицы воротника')


class CuffType(ComponentModel):
    rounding = models.ManyToManyField('CuffRounding', verbose_name=_(u'Варианты закругления'), blank=True)

    class Meta:
        verbose_name = _(u'Тип манжеты')
        verbose_name_plural = _(u'Типы манжет')


class CuffRounding(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    types = models.ManyToManyField('CuffType', verbose_name=_(u'Типы'), through=CuffType.rounding.through, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Тип закругления манжеты')
        verbose_name_plural = _(u'Типы закругления манжеты')


class CustomButtonsType(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    extra_price = models.DecimalField(_(u'Добавочная стоимость'), decimal_places=2, max_digits=10)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Тип пуговиц')
        verbose_name_plural = _(u'Типы пуговиц')

    def get_shirts(self):
        return self.back_shirts.filter(custom_buttons__isnull=False).values('id')


class YokeType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип кокетки')
        verbose_name_plural = _(u'Типы кокетки')


class StitchColor(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    color = RGBColorField(_(u'Цвет'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Цвет отстрочки')
        verbose_name_plural = _(u'Цвета отстрочки')


class DickeyType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип манишки')
        verbose_name_plural = _(u'Типы манишки')


class ShirtInfo(models.Model):
    title = models.CharField(_(u'Заголовок'), max_length=255, unique=True)
    text = models.TextField(_(u'Текст под заголовком'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Информация о рубашках')
        verbose_name_plural = _(u'Информация о рубашках')

class ShirtInfoImage(models.Model):
    image = models.ImageField(_(u'Файл'))
    text = models.TextField(_(u'Текст под изображением'))
    shirt_info = models.ForeignKey(ShirtInfo, related_name='images')

    class Meta:
        verbose_name = _(u'Изображение')
        verbose_name_plural = _(u'Изображения')


class SizeOptions(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    show_sizes = models.BooleanField(_(u'Показывать размеры'), default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Вариант размера')
        verbose_name_plural = _(u'Варианты размеров')


class Size(models.Model):
    size = models.PositiveIntegerField(_(u'Размер'), unique=True, primary_key=True)

    def __unicode__(self):
        return "%s" % self.size

    class Meta:
        verbose_name = _(u'Размер рубашки')
        verbose_name_plural = _(u'Размеры рубашек')


class HemType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип низа')
        verbose_name_plural = _(u'Типы низа')


class SleeveType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип рукава')
        verbose_name_plural = _(u'Типы рукавов')


class PlacketType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип полочки')
        verbose_name_plural = _(u'Типы полочек')


class PocketType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип кармана')
        verbose_name_plural = _(u'Типы карманов')


class BackType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип спинки')
        verbose_name_plural = _(u'Типы спинок')


class Thickness(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)

    class Meta:
        verbose_name = _(u'Толщина ткани')
        verbose_name_plural = _(u'Толщина ткани')

    def __unicode__(self):
        return self.title
