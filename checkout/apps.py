# coding: utf-8

from django.apps import AppConfig
from django.utils.text import ugettext_lazy as _


class CheckoutConfig(AppConfig):
    name = 'checkout'
    verbose_name = _(u'Магазин')
