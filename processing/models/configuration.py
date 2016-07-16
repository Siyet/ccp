# coding: utf-8

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import ugettext_lazy as _

from dictionaries import models as dictionaries
from backend import models as backend
from processing.upload_path import UploadComposingSource
from processing.storage import overwrite_storage


class ConfigurationModel(models.Model):
    def __unicode__(self):
        return "#%s" % self.id

    class Meta:
        abstract = True


class PartConfigurationModel(ConfigurationModel):
    sources = GenericRelation('processing.ComposeSource')

    class Meta:
        abstract = True

class ButtonsConfigurationModel(ConfigurationModel):
    sources = GenericRelation('processing.ButtonsSource')

    class Meta:
        abstract = True


class BodyConfiguration(PartConfigurationModel):
    sleeve = models.ForeignKey(dictionaries.SleeveType, verbose_name=_(u'Рукав'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))
    cuff_types = models.ManyToManyField(dictionaries.CuffType, verbose_name=_(u'Типы манжет'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для основы')
        verbose_name_plural = _(u'Конфигурации сборки для основы')


class BackConfiguration(PartConfigurationModel):
    back = models.ForeignKey(dictionaries.BackType, verbose_name=_(u'Спинка'))
    tuck = models.BooleanField(verbose_name=_(u'Вытачки'), choices=backend.Shirt.TUCK_OPTIONS, default=False)
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))

    class Meta:
        unique_together = ('back', 'hem', 'tuck')
        verbose_name = _(u'Конфигурация сборки для спинки')
        verbose_name_plural = _(u'Конфигурации сборки для спинки')


class CollarConfiguration(PartConfigurationModel):
    collar = models.ForeignKey(dictionaries.CollarType, verbose_name=_(u'Воротник'))
    buttons = models.IntegerField(_(u'Количество пуговиц'), choices=dictionaries.CollarButtons.BUTTONS_CHOICES,
                                  default=1)

    class Meta:
        unique_together = ('collar', 'buttons')
        verbose_name = _(u'Конфигурация сборки для воротника')
        verbose_name_plural = _(u'Конфигурации сборки для воротника')


class CuffConfiguration(PartConfigurationModel):
    cuff_types = models.ManyToManyField(dictionaries.CuffType, verbose_name=_(u'Типы манжет'))
    rounding = models.ForeignKey(dictionaries.CuffRounding, verbose_name=_(u'Тип закругления'), blank=True, null=True)
    side_mask = models.FileField(verbose_name=_(u'Маска рукава (сбоку)'), storage=overwrite_storage,
                                   upload_to=UploadComposingSource('composesource/%s/%s'), null=True)

    class Meta:
        verbose_name = _(u'Конфигурация сборки для манжет')
        verbose_name_plural = _(u'Конфигурации сборки для манжет')


class PocketConfiguration(PartConfigurationModel):
    pocket = models.OneToOneField(dictionaries.PocketType, verbose_name=_(u'Тип кармана'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для кармана')
        verbose_name_plural = _(u'Конфигурации сборки для кармана')


class PlacketConfiguration(PartConfigurationModel):
    placket = models.ForeignKey(dictionaries.PlacketType, verbose_name=_(u'Тип полочки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))

    class Meta:
        unique_together = ('placket', 'hem')
        verbose_name = _(u'Конфигурация сборки для полочки')
        verbose_name_plural = _(u'Конфигурации сборки для полочки')


class DickeyConfiguration(PartConfigurationModel):
    dickey = models.ForeignKey(dictionaries.DickeyType, verbose_name=_(u'Тип манишки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'), null=True, blank=True)

    class Meta:
        unique_together = ('dickey', 'hem')
        verbose_name = _(u'Конфигурация сборки для манишки')
        verbose_name_plural = _(u'Конфигурации сборки для манишки')


class BodyButtonsConfiguration(ButtonsConfigurationModel):
    buttons = models.OneToOneField(dictionaries.CustomButtonsType, verbose_name=_(u'Пуговицы'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для основных пуговиц')
        verbose_name_plural = _(u'Конфигурации сборки для основных пуговиц')


class CollarButtonsConfiguration(ButtonsConfigurationModel):
    collar = models.ForeignKey(dictionaries.CollarType, verbose_name=_(u'Воротник'))
    buttons = models.IntegerField(_(u'Количество пуговиц'), choices=dictionaries.CollarButtons.BUTTONS_CHOICES,
                                  default=1)

    class Meta:
        unique_together = ('collar', 'buttons')
        verbose_name = _(u'Конфигурация сборки для пуговиц воротника')
        verbose_name_plural = _(u'Конфигурации сборки для пуговиц воротника')


class CuffButtonsConfiguration(ButtonsConfigurationModel):
    cuff = models.ForeignKey(dictionaries.CuffType, verbose_name=_(u'Тип мажеты'))
    rounding_types = models.ManyToManyField(dictionaries.CuffRounding, verbose_name=_(u'Типы закругления'), blank=True)

    class Meta:
        verbose_name = _(u'Конфигурация сборки для пуговиц манжет')
        verbose_name_plural = _(u'Конфигурации сборки для пуговиц манжет')
