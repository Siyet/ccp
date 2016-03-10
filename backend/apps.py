# coding: utf-8

from django.apps import AppConfig
from django.utils.text import ugettext_lazy as _

class BackendConfig(AppConfig):
    name = 'backend'
    verbose_name = _(u'Конфигуратор')

    def ready(self):
        import backend.signals
