# coding: utf-8

from django.db import models
from processing.models.configuration import *
from dictionaries import models as dictionaries

from django.utils.translation import ugettext_lazy as _
from processing.models.configuration import UnisexModel
from backend import models as backend


class WomanConfigurationManager(models.Manager):
    def get_queryset(self):
        qs = super(self, WomanConfigurationManager).get_queryset()
        return qs.filter(sex=backend.SEX.female)


class WomanConfigurationModel(models.Model):
    objects = WomanConfigurationManager()

    def save(self, *args, **kwargs):
        self.sex = backend.SEX.female
        super(self, WomanConfigurationModel).save(*args, **kwargs)

    class Meta:
        abstract = True


class WomanBodyConfiguration(models.Model):
    pass


class WomanCollarConfiguration(PartConfigurationModel):
    collar = models.OneToOneField(dictionaries.CollarType, verbose_name=_(u'Воротник'))
    masks = GenericRelation('processing.CollarMask')

    class Meta:
        verbose_name = _(u'Конфигурация сборки для воротника')
        verbose_name_plural = _(u'Конфигурации сборки для воротника')


class WomanCuffConfiguration(CuffConfiguration):
    class Meta:
        proxy = True


class WomanPocketConfiguration(WomanConfigurationModel, PocketConfiguration):
    class Meta:
        proxy = True


class WomanPlacketConfiguration(PartConfigurationModel):
    plackets = models.ManyToManyField(dictionaries.PlacketType, verbose_name=_(u'Тип полочки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))
    tuck = models.ForeignKey(dictionaries.TuckType, verbose_name=_(u'Вытачки'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для полочки')
        verbose_name_plural = _(u'Конфигурации сборки для полочки')


class WomanYokeConfiguration(WomanConfigurationModel, YokeConfiguration):
    class Meta:
        proxy = True


class WomanBodyButtonsConfiguration(WomanConfigurationModel, BodyButtonsConfiguration):
    class Meta:
        proxy = True


class WomanCollarButtonsConfiguration(ButtonsConfigurationModel):
    collar = models.OneToOneField(dictionaries.CollarType, verbose_name=_(u'Воротник'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для пуговиц воротника')
        verbose_name_plural = _(u'Конфигурации сборки для пуговиц воротника')


class WomanCuffButtonsConfiguration(WomanConfigurationModel, CuffButtonsConfiguration):
    class Meta:
        proxy = True


class WomanInitialsConfiguration(WomanConfigurationModel, InitialsConfiguration):
    class Meta:
        proxy = True
