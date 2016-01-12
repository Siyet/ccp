# coding: utf-8

from django.apps import AppConfig
from django.utils.text import ugettext_lazy as _

class ProcessingConfig(AppConfig):
    name = 'processing'
    verbose_name = _(u'Рендеринг')