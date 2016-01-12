# coding: utf-8

from django.apps import AppConfig
from django.utils.text import ugettext_lazy as _

class DictionariesConfig(AppConfig):
    name = 'dictionaries'
    verbose_name = _(u'Справочники')