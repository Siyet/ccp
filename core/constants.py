# coding: utf-8

from model_utils.choices import Choices
from django.utils.translation import ugettext_lazy as _

SEX = Choices(
    ('male', _(u'Мужская')),
    ('female', _(u'Женская')),
    ('unisex', _(u'Унисекс')),
)
