# coding: utf-8

from django.db import models
from django.utils.text import ugettext_lazy as _
from model_utils import Choices
from colorful.fields import RGBColorField

class Color(models.Model):
    color = RGBColorField(_(u'Значение'))

    def __unicode__(self):
        return self.color

    class Meta:
        verbose_name = u'Цвет (для инициалов)'
        verbose_name_plural = u'Цвета (для инициалов)'


class FabricColor(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    value = RGBColorField(_(u'Значение'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Цвет ткани')
        verbose_name_plural = _(u'Цвета тканей')


class FabricCategory(models.Model):
    title = models.CharField(_(u'Категория'), unique=True, max_length=1)

    def __unicode__(self):
        return u"%s %s" % (_(u'Категория'), self.title)
    class Meta:
        verbose_name = _(u'Категория ткани')
        verbose_name_plural = _(u'Категории тканей')


class CollarButtons(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Пуговицы воротника')
        verbose_name_plural = _(u'Пуговицы воротника')


class FabricDesign(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    picture = models.ImageField(_(u'Изображение'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Паттерн ткани')
        verbose_name_plural = _(u'Паттерны тканей')


class CollarType(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    buttons = models.ManyToManyField(CollarButtons, verbose_name=_(u'Варианты пуговиц'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Тип воротника')
        verbose_name_plural = _(u'Типы воротников')


class CuffRounding(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Тип закругления манжеты')
        verbose_name_plural = _(u'Типы закругления манжеты')


class CuffType(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    rounding = models.ManyToManyField(CuffRounding, verbose_name=_(u'Варианты закругления'), blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Тип манжеты')
        verbose_name_plural = _(u'Типы манжет')


class CustomButtonsType(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    extra_price = models.DecimalField(_(u'Добавочная стоимость'), decimal_places=2, max_digits=10)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Тип пуговиц')
        verbose_name_plural = _(u'Типы пуговиц')


class YokeType(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    picture = models.ImageField(_(u'Изображение'))

    def __unicode__(self):
        return self.title

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


class DickeyType(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    picture = models.ImageField(_(u'Изображение'))

    def __unicode__(self):
        return self.title

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
