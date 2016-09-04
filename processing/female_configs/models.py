# coding: utf-8

from django.db import models
from processing.models.configuration import *
from dictionaries import models as dictionaries

from django.utils.translation import ugettext_lazy as _
from processing.models.configuration import UnisexModel
from processing.models.sources import ComposeSource
from core.constants import SEX


class FemaleConfigurationManager(models.Manager):
    def get_queryset(self):
        qs = super(FemaleConfigurationManager, self).get_queryset()
        return qs.filter(sex=SEX.female)


class FemaleConfigurationModel(models.Model):
    objects = FemaleConfigurationManager()

    def save(self, *args, **kwargs):
        self.sex = SEX.female
        super(FemaleConfigurationModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class FemaleBodyConfiguration(PartConfigurationModel):
    sleeve = models.ForeignKey(dictionaries.SleeveType, verbose_name=_(u'Рукав'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))
    cuff_types = models.ManyToManyField(dictionaries.CuffType, verbose_name=_(u'Типы манжет'))
    tuck = models.ForeignKey(dictionaries.TuckType, verbose_name=_(u'Вытачки'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для основы')
        verbose_name_plural = _(u'Конфигурации сборки для основы')


class FemaleCollarConfiguration(PartConfigurationModel):
    collar = models.OneToOneField(dictionaries.CollarType, verbose_name=_(u'Воротник'))
    masks = GenericRelation('processing.CollarMask')

    class Meta:
        verbose_name = _(u'Конфигурация сборки для воротника')
        verbose_name_plural = _(u'Конфигурации сборки для воротника')


class FemaleCuffConfiguration(CuffConfiguration):
    class Meta:
        proxy = True
        verbose_name = CuffConfiguration._meta.verbose_name
        verbose_name_plural = CuffConfiguration._meta.verbose_name_plural


class FemalePocketConfiguration(FemaleConfigurationModel, PocketConfiguration):
    class Meta:
        proxy = True
        verbose_name = PocketConfiguration._meta.verbose_name
        verbose_name_plural = PocketConfiguration._meta.verbose_name_plural


class FemalePlacketConfiguration(PartConfigurationModel):
    plackets = models.ManyToManyField(dictionaries.PlacketType, verbose_name=_(u'Тип полочки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))
    tuck = models.ForeignKey(dictionaries.TuckType, verbose_name=_(u'Вытачки'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для полочки')
        verbose_name_plural = _(u'Конфигурации сборки для полочки')


class FemaleYokeConfiguration(FemaleConfigurationModel, YokeConfiguration):
    class Meta:
        proxy = True
        verbose_name = YokeConfiguration._meta.verbose_name
        verbose_name_plural = YokeConfiguration._meta.verbose_name_plural


class FemaleBodyButtonsConfiguration(FemaleConfigurationModel, BodyButtonsConfiguration):
    class Meta:
        proxy = True
        verbose_name = BodyButtonsConfiguration._meta.verbose_name
        verbose_name_plural = BodyButtonsConfiguration._meta.verbose_name_plural


class FemaleCollarButtonsConfiguration(ButtonsConfigurationModel):
    collar = models.OneToOneField(dictionaries.CollarType, verbose_name=_(u'Воротник'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для пуговиц воротника')
        verbose_name_plural = _(u'Конфигурации сборки для пуговиц воротника')


class FemaleCuffButtonsConfiguration(FemaleConfigurationModel, CuffButtonsConfiguration):
    class Meta:
        proxy = True
        verbose_name = CuffButtonsConfiguration._meta.verbose_name
        verbose_name_plural = CuffButtonsConfiguration._meta.verbose_name_plural


class FemaleInitialsConfiguration(FemaleConfigurationModel, InitialsConfiguration):
    class Meta:
        proxy = True
        verbose_name = InitialsConfiguration._meta.verbose_name
        verbose_name_plural = InitialsConfiguration._meta.verbose_name_plural


class FemaleBodySource(ComposeSource):
    back = models.ForeignKey('dictionaries.BackType', verbose_name=_(u'Спинка'), null=True, blank=True)


class FemaleBackShadow(CachedSource):
    back = models.OneToOneField('dictionaries.BackType', verbose_name=_(u'Спинка'))
    models.FileField(verbose_name=_(u'Файл тени'), storage=overwrite_storage,
                             upload_to=UploadComposingSource('composesource/%s/%s'))

    def __unicode__(self):
        return _(u'Тень для спинки: %s') % self.back.title

    class Meta:
        verbose_name = _(u'Тень спинки')
        verbose_name_plural = _(u'Тени спинки')
