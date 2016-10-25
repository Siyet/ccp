# coding: utf-8

from django.utils.text import ugettext_lazy as _

from processing.models.configuration import *
from processing.models.sources import CachedSource
from dictionaries import models as dictionaries
from core.constants import SEX


class MaleConfigurationManager(models.Manager):
    def get_queryset(self):
        qs = super(MaleConfigurationManager, self).get_queryset()
        return qs.filter(sex=SEX.male)


class MaleConfigurationModel(models.Model):
    objects = MaleConfigurationManager()

    def save(self, *args, **kwargs):
        self.sex = SEX.male
        super(MaleConfigurationModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class MaleBodyConfiguration(PartConfigurationModel):
    sleeve = models.ForeignKey(dictionaries.SleeveType, verbose_name=_(u'Рукав'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))
    cuff_types = models.ManyToManyField(dictionaries.CuffType, verbose_name=_(u'Типы манжет'), blank=True)

    class Meta:
        verbose_name = _(u'Конфигурация сборки для основы')
        verbose_name_plural = _(u'Конфигурации сборки для основы')


class MaleBackConfiguration(PartConfigurationModel):
    back = models.ForeignKey(dictionaries.BackType, verbose_name=_(u'Спинка'))
    tuck = models.ForeignKey(dictionaries.TuckType, verbose_name=_(u'Вытачки'))

    class Meta:
        unique_together = ('back', 'tuck')
        verbose_name = _(u'Конфигурация сборки для спинки')
        verbose_name_plural = _(u'Конфигурации сборки для спинки')


class MaleCollarConfiguration(PartConfigurationModel):
    collar = models.ForeignKey(dictionaries.CollarType, verbose_name=_(u'Воротник'))
    buttons = models.IntegerField(_(u'Количество пуговиц'), choices=dictionaries.CollarButtons.BUTTONS_CHOICES,
                                  default=1)
    masks = GenericRelation('processing.CollarMask')

    class Meta:
        unique_together = ('collar', 'buttons')
        verbose_name = _(u'Конфигурация сборки для воротника')
        verbose_name_plural = _(u'Конфигурации сборки для воротника')


class MaleCuffConfiguration(MaleConfigurationModel, CuffConfiguration):
    class Meta:
        proxy = True
        verbose_name = CuffConfiguration._meta.verbose_name
        verbose_name_plural = CuffConfiguration._meta.verbose_name_plural


class MalePocketConfiguration(MaleConfigurationModel, PocketConfiguration):
    class Meta:
        proxy = True
        verbose_name = PocketConfiguration._meta.verbose_name
        verbose_name_plural = PocketConfiguration._meta.verbose_name_plural


class MalePlacketConfiguration(PartConfigurationModel):
    plackets = models.ManyToManyField(dictionaries.PlacketType, verbose_name=_(u'Тип полочки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для полочки')
        verbose_name_plural = _(u'Конфигурации сборки для полочки')


class DickeyConfiguration(PartConfigurationModel):
    dickey = models.ForeignKey(dictionaries.DickeyType, verbose_name=_(u'Тип манишки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'), null=True, blank=True)

    class Meta:
        unique_together = ('dickey', 'hem')
        verbose_name = _(u'Конфигурация сборки для манишки')
        verbose_name_plural = _(u'Конфигурации сборки для манишки')


class MaleYokeConfiguration(MaleConfigurationModel, YokeConfiguration):
    class Meta:
        proxy = True
        verbose_name = YokeConfiguration._meta.verbose_name
        verbose_name_plural = YokeConfiguration._meta.verbose_name_plural


class MaleBodyButtonsConfiguration(MaleConfigurationModel, BodyButtonsConfiguration):
    class Meta:
        proxy = True
        verbose_name = BodyButtonsConfiguration._meta.verbose_name
        verbose_name_plural = BodyButtonsConfiguration._meta.verbose_name_plural


class MaleCollarButtonsConfiguration(ButtonsConfigurationModel):
    collar = models.ForeignKey(dictionaries.CollarType, verbose_name=_(u'Воротник'))
    buttons = models.IntegerField(_(u'Количество пуговиц'), choices=dictionaries.CollarButtons.BUTTONS_CHOICES,
                                  default=1)

    class Meta:
        unique_together = ('collar', 'buttons')
        verbose_name = _(u'Конфигурация сборки для пуговиц воротника')
        verbose_name_plural = _(u'Конфигурации сборки для пуговиц воротника')


class MaleCuffButtonsConfiguration(MaleConfigurationModel, CuffButtonsConfiguration):
    class Meta:
        proxy = True
        verbose_name = CuffButtonsConfiguration._meta.verbose_name
        verbose_name_plural = CuffButtonsConfiguration._meta.verbose_name_plural


class MaleInitialsConfiguration(MaleConfigurationModel, InitialsConfiguration):
    class Meta:
        proxy = True
        verbose_name = InitialsConfiguration._meta.verbose_name
        verbose_name_plural = InitialsConfiguration._meta.verbose_name_plural
