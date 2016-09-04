# coding: utf-8

from rest_framework import filters
import django_filters

from core.constants import SEX
from backend import models
from django.utils.translation import ugettext as _

from django_filters.fields import Lookup
from django_filters.filters import BaseInFilter, MultipleChoiceFilter
from django import forms
from django.utils.encoding import smart_text


class CSVChoiceField(forms.MultipleChoiceField):
    def to_python(self, value):
        value = super(CSVChoiceField, self).to_python(value)
        if not value:
            return []
        values = ','.join(value).split(',')
        print(values)
        return [smart_text(val) for val in values]


class CSVMultipleChoiceFilter(MultipleChoiceFilter):
    field_class = CSVChoiceField


class TemplateShirtsFilter(filters.FilterSet):
    fabric = BaseInFilter(label=_(u'Ткань'))
    fabric__type = BaseInFilter(label=_(u'Тип ткани'))
    fabric__colors = BaseInFilter(label=_(u'Цвет ткани'))
    fabric__designs = BaseInFilter(label=_(u'Паттерн ткани'))
    fabric__thickness = BaseInFilter(label=_(u'Толщина ткани'))
    collection = BaseInFilter(label=_(u'Коллекция'))
    collection__sex = CSVMultipleChoiceFilter(choices=SEX, label=_(u'Пол коллекции'), lookup_expr='in')

    class Meta:
        model = models.Shirt
        fields = [] # include only explicitly specified fields


class CollectionFabricsFilter(filters.FilterSet):
    class Meta:
        model = models.Fabric
        fields = ('colors', 'designs', 'type', 'thickness',)
