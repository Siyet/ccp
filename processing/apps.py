# coding: utf-8

from django.apps import AppConfig
from django.utils.text import ugettext_lazy as _

class ProcessingConfig(AppConfig):
    name = 'processing'
    verbose_name = _(u'Рендеринг')

    def ready(self):
        # noinspection PyUnresolvedReferences
        from processing import signals


class ManProcessingConfig(AppConfig):
    name = 'processing.male_configs'
    verbose_name = _(u'Рендеринг (мужчины)')


class WomanProcessingConfig(AppConfig):
    name = 'processing.female_configs'
    verbose_name = _(u'Рендеринг (женщины)')
