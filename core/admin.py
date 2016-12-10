# coding: utf-8

from .utils import first
from django.utils.translation import ugettext_lazy as _

class ManyToManyListFormatter(object):
    def __init__(self, field, description, separator=', '):
        self.field = field
        self.separator = separator
        self.short_description = description

    def __call__(self, obj):
        m2m_manager = getattr(obj, self.field)
        return self.separator.join([unicode(related) for related in m2m_manager.all()]) or _(u"(Нет)")


class ManyToManyMixin(object):
    m2m_fields = []

    def get_list_display(self, request):
        list_display = self.get_fields(request)
        present_fields = filter(lambda f: f in list_display, self.m2m_fields)
        for field_name in present_fields:
            field_idx = list_display.index(field_name)
            m2m_field = first(lambda x: x.name == field_name, self.model._meta.many_to_many)
            assert m2m_field is not None
            formatter = ManyToManyListFormatter(field_name, m2m_field.verbose_name)

            field_attr = list_display[field_idx] + "_list"
            list_display[field_idx] = field_attr
            setattr(self, field_attr, formatter)
        return list_display

    def get_queryset(self, request):
        fields = self.get_fields(request)
        prefetch_fields = filter(lambda f: f in fields, self.m2m_fields)
        return super(ManyToManyMixin, self).get_queryset(request).prefetch_related(*prefetch_fields)