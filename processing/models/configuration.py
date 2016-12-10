# coding: utf-8

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import ugettext_lazy as _

from backend import models as backend
from core.constants import SEX
from dictionaries import models as dictionaries
from processing.storage import overwrite_storage
from processing.upload_path import UploadComposingSource


class CachedSource(models.Model):
    cache = GenericRelation('processing.SourceCache')

    class Meta:
        abstract = True


class ConfigurationModel(models.Model):
    def __unicode__(self):
        return "#%s" % self.id

    class Meta:
        abstract = True


class UnisexModel(models.Model):
    sex = models.CharField(max_length=10, choices=SEX, default=SEX.male)

    class Meta:
        abstract = True


class PartConfigurationModel(ConfigurationModel):
    sources = GenericRelation('processing.ComposeSource')

    class Meta:
        abstract = True


class ButtonsConfigurationModel(ConfigurationModel):
    sources = GenericRelation('processing.ButtonsSource')
    stitches = GenericRelation('processing.StitchesSource')

    class Meta:
        abstract = True


class CuffConfiguration(UnisexModel, CachedSource, PartConfigurationModel):
    cuff_types = models.ManyToManyField(dictionaries.CuffType, verbose_name=_(u'Типы манжет'))
    rounding = models.ForeignKey(dictionaries.CuffRounding, verbose_name=_(u'Тип закругления'), blank=True, null=True)
    side_mask = models.FileField(verbose_name=_(u'Маска рукава (сбоку)'), storage=overwrite_storage,
                                 upload_to=UploadComposingSource('composesource/%s/%s'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Конфигурация сборки для манжет')
        verbose_name_plural = _(u'Конфигурации сборки для манжет')


class PocketConfiguration(UnisexModel, PartConfigurationModel):
    pocket = models.ForeignKey(dictionaries.PocketType, verbose_name=_(u'Тип кармана'))

    class Meta:
        unique_together = ('pocket', 'sex')
        verbose_name = _(u'Конфигурация сборки для кармана')
        verbose_name_plural = _(u'Конфигурации сборки для кармана')


class YokeConfiguration(UnisexModel, PartConfigurationModel):
    yoke = models.ForeignKey(dictionaries.YokeType, verbose_name=_(u'Тип кокетки'))

    class Meta:
        unique_together = ('yoke', 'sex')
        verbose_name = _(u'Конфигурация сборки для кокетки')
        verbose_name_plural = _(u'Конфигурации сборки для кокетки')


class BodyButtonsConfiguration(UnisexModel, ButtonsConfigurationModel):
    plackets = models.ManyToManyField('dictionaries.PlacketType', verbose_name=_(u'Тип полочки'))
    class Meta:
        verbose_name = _(u'Конфигурация сборки для основных пуговиц')
        verbose_name_plural = _(u'Конфигурации сборки для основных пуговиц')


class CuffButtonsConfiguration(UnisexModel, ButtonsConfigurationModel):
    cuff = models.ForeignKey(dictionaries.CuffType, verbose_name=_(u'Тип мажеты'))
    rounding_types = models.ManyToManyField(dictionaries.CuffRounding, verbose_name=_(u'Типы закругления'), blank=True)

    class Meta:
        verbose_name = _(u'Конфигурация сборки для пуговиц манжет')
        verbose_name_plural = _(u'Конфигурации сборки для пуговиц манжет')


class StitchColor(models.Model):
    content_type = models.OneToOneField(ContentType, verbose_name=_(u'Тип конфигурации'), limit_choices_to={
        'model__in': ('bodybuttonsconfiguration', 'cuffbuttonsconfiguration', 'malecollarbuttonsconfiguration',
                      'femalecollarbuttonsconfiguration')
    })
    element = models.ForeignKey(backend.ElementStitch, verbose_name=_(u'Отстрочка'))

    class Meta:
        verbose_name = _(u'Конфигурация отстрочки')
        verbose_name_plural = _(u'Конфигурации отстрочек')

    def __unicode__(self):
        return unicode(self.content_type)


class InitialsConfiguration(UnisexModel, ConfigurationModel):
    font = models.ForeignKey(dictionaries.Font, verbose_name=_(u'Шрифт'))
    font_size = models.IntegerField(_(u'Размер шрифта'), default=18)
    pocket = models.ManyToManyField(dictionaries.PocketType, verbose_name=_(u'Видно с карманом'))
    location = models.CharField(_(u'Местоположение'), choices=backend.Initials.LOCATION, max_length=10)

    class Meta:
        verbose_name = _(u'Конфигурация инициалов')
        verbose_name_plural = _(u'Конфигурации инициалов')
