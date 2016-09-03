# coding: utf-8

from django.utils.text import ugettext_lazy as _

from processing.models.configuration import *
from processing.models.sources import CachedSource
from dictionaries import models as dictionaries
from backend import models as backend


class ManConfigurationManager(models.Manager):
    def get_queryset(self):
        qs = super(self, ManConfigurationManager).get_queryset()
        return qs.filter(sex=backend.SEX.male)


class ManConfigurationModel(models.Model):
    objects = ManConfigurationManager()

    def save(self, *args, **kwargs):
        self.sex = backend.SEX.male
        super(self, ManConfigurationModel).save(*args, **kwargs)

    class Meta:
        abstract = True


class ManBodyConfiguration(UnisexModel, PartConfigurationModel):
    sleeve = models.ForeignKey(dictionaries.SleeveType, verbose_name=_(u'Рукав'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))
    cuff_types = models.ManyToManyField(dictionaries.CuffType, verbose_name=_(u'Типы манжет'))

    class Meta:
        db_table = 'processing_bodyconfiguration'
        verbose_name = _(u'Конфигурация сборки для основы')
        verbose_name_plural = _(u'Конфигурации сборки для основы')


class ManBackConfiguration(PartConfigurationModel):
    back = models.ForeignKey(dictionaries.BackType, verbose_name=_(u'Спинка'))
    tuck = models.ForeignKey(dictionaries.TuckType, verbose_name=_(u'Вытачки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))

    class Meta:
        db_table = 'processing_backconfiguration'
        unique_together = ('back', 'hem', 'tuck')
        verbose_name = _(u'Конфигурация сборки для спинки')
        verbose_name_plural = _(u'Конфигурации сборки для спинки')


class ManCollarConfiguration(PartConfigurationModel):
    collar = models.ForeignKey(dictionaries.CollarType, verbose_name=_(u'Воротник'))
    buttons = models.IntegerField(_(u'Количество пуговиц'), choices=dictionaries.CollarButtons.BUTTONS_CHOICES,
                                  default=1)
    masks = GenericRelation('processing.CollarMask')

    class Meta:
        db_table = 'processing_collarconfiguration'
        unique_together = ('collar', 'buttons')
        verbose_name = _(u'Конфигурация сборки для воротника')
        verbose_name_plural = _(u'Конфигурации сборки для воротника')


class ManCuffConfiguration(CuffConfiguration, CachedSource, ManConfigurationModel):
    class Meta:
        proxy = True


class ManPocketConfiguration(ManConfigurationModel, PocketConfiguration):
    class Meta:
        proxy = True


class ManPlacketConfiguration(PartConfigurationModel):
    plackets = models.ManyToManyField(dictionaries.PlacketType, verbose_name=_(u'Тип полочки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))

    class Meta:
        db_table = 'processing_placketconfiguration'
        verbose_name = _(u'Конфигурация сборки для полочки')
        verbose_name_plural = _(u'Конфигурации сборки для полочки')


class DickeyConfiguration(PartConfigurationModel):
    dickey = models.ForeignKey(dictionaries.DickeyType, verbose_name=_(u'Тип манишки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'), null=True, blank=True)

    class Meta:
        db_table = 'processing_dickeyconfiguration'
        unique_together = ('dickey', 'hem')
        verbose_name = _(u'Конфигурация сборки для манишки')
        verbose_name_plural = _(u'Конфигурации сборки для манишки')


class ManYokeConfiguration(ManConfigurationModel, YokeConfiguration):
    class Meta:
        proxy = True


class ManBodyButtonsConfiguration(ManConfigurationModel, BodyButtonsConfiguration):
    class Meta:
        proxy = True


class ManCollarButtonsConfiguration(ButtonsConfigurationModel):
    collar = models.ForeignKey(dictionaries.CollarType, verbose_name=_(u'Воротник'))
    buttons = models.IntegerField(_(u'Количество пуговиц'), choices=dictionaries.CollarButtons.BUTTONS_CHOICES,
                                  default=1)

    class Meta:
        db_table = 'processing_collarbuttonsconfiguration'
        unique_together = ('collar', 'buttons')
        verbose_name = _(u'Конфигурация сборки для пуговиц воротника')
        verbose_name_plural = _(u'Конфигурации сборки для пуговиц воротника')


class ManCuffButtonsConfiguration(ManConfigurationModel, CuffButtonsConfiguration):
    class Meta:
        proxy = True


class ManInitialsConfiguration(ManConfigurationModel, InitialsConfiguration):
    class Meta:
        proxy = True
