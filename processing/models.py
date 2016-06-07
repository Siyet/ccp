# coding: UTF-8

from django.db import models
from dictionaries import models as dictionaries
from model_utils.choices import Choices
from django.utils.text import ugettext_lazy as _

from upload_path import UploadComposingSource

from backend import models as backend

class SourceMixin(object):

    def __unicode__(self):
        return "#%s" % self.id


class BodySource(models.Model, SourceMixin):
    sleeve = models.ForeignKey(dictionaries.SleeveType, verbose_name=_(u'Рукав'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))
    cuff = models.ForeignKey(dictionaries.CuffType, verbose_name=_(u'Манжет'), blank=True, null=True)

    class Meta:
        unique_together = ('sleeve', 'hem', 'cuff')
        verbose_name = _(u'Конфигурация сборки для основы')
        verbose_name_plural = _(u'Конфигурации сборки для основы')



class BackSource(models.Model, SourceMixin):
    back = models.ForeignKey(dictionaries.BackType, verbose_name=_(u'Спинка'))
    tuck = models.BooleanField(verbose_name=_(u'Вытачки'), choices=backend.Shirt.TUCK_OPTIONS, default=False)
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))

    class Meta:
        unique_together = ('back', 'hem', 'tuck')
        verbose_name = _(u'Конфигурация сборки для спинки')
        verbose_name_plural = _(u'Конфигурации сборки для спинки')

class CollarSource(models.Model, SourceMixin):
    collar = models.OneToOneField(dictionaries.CollarType, verbose_name=_(u'Воротник'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для воротника')
        verbose_name_plural = _(u'Конфигурации сборки для воротника')


class CuffSource(models.Model, SourceMixin):
    cuff = models.ForeignKey(dictionaries.CuffType, verbose_name=_(u'Тип манжеты'))
    rounding = models.ForeignKey(dictionaries.CuffRounding, verbose_name=_(u'Тип закругления'), blank=True, null=True)

    class Meta:
        unique_together = ('cuff', 'rounding')
        verbose_name = _(u'Конфигурация сборки для манжет')
        verbose_name_plural = _(u'Конфигурации сборки для манжет')


class PocketSource(models.Model, SourceMixin):
    pocket = models.OneToOneField(dictionaries.PocketType, verbose_name=_(u'Тип кармана'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для кармана')
        verbose_name_plural = _(u'Конфигурации сборки для кармана')


class PlacketSource(models.Model, SourceMixin):
    placket = models.OneToOneField(dictionaries.PlacketType, verbose_name=_(u'Тип полочки'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для полочки')
        verbose_name_plural = _(u'Конфигурации сборки для полочки')


class ComposeSource(models.Model):
    PROJECTION = Choices(("front", _(u'Передняя')), ("side", _(u"Боковая")), ("back", _(u'Задняя')))

    uv = models.FileField(_(u'UV'), upload_to=UploadComposingSource('%s/uv/%s'))
    ao = models.FileField(_(u'Тени'), upload_to=UploadComposingSource('%s/ao/%s'))
    light = models.FileField(_(u'Свет'), upload_to=UploadComposingSource('%s/light/%s'))
    projection = models.CharField(_(u'Проекция'), max_length=5, choices=PROJECTION)

    cuff_source = models.ForeignKey(CuffSource, blank=True, null=True)
    back_source = models.ForeignKey(BackSource, blank=True, null=True)
    collar_source = models.ForeignKey(CollarSource, blank=True, null=True)
    body_source = models.ForeignKey(BodySource, blank=True, null=True)
    placket_source = models.ForeignKey(PlacketSource, blank=True, null=True)
    pocket_source = models.ForeignKey(PocketSource, blank=True, null=True)

    class Meta:
        verbose_name = _(u'Модель сборки')
        verbose_name_plural = _(u'Модели сборки')


class Texture(models.Model):
    TILING = Choices((4, "default", _(u'Стандартный')), (8, "frequent", _(u'Учащенный (х2)')))

    texture = models.ImageField(_(u'Файл текстуры'))
    tiling = models.PositiveIntegerField(_(u'Тайлинг'), choices=TILING, default=TILING.default)
    needs_shadow = models.BooleanField(_(u'Использовать тени'), default=True)

    class Meta:
        verbose_name = _(u'Текстура')
        verbose_name_plural = _(u'Текстуры')

