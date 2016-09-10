# coding: utf-8

from django.contrib import admin
from imagekit.admin import AdminThumbnail
from django.utils.text import ugettext_lazy as _
from django.contrib.contenttypes.admin import GenericTabularInline

import models
from core.utils import first


class ManyToManyListFormatter(object):
    def __init__(self, field, description, separator=', '):
        self.field = field
        self.separator = separator
        self.short_description = description

    def __call__(self, obj):
        m2m_manager = getattr(obj, self.field)
        return self.separator.join([unicode(related) for related in m2m_manager.all()])


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


class CollarMaskInline(GenericTabularInline):
    model = models.CollarMask
    max_num = 12
    fields = ('projection', 'mask', 'element')


class ComposingSourceInline(GenericTabularInline):
    model = models.ComposeSource
    fields = ('projection', 'uv', 'ao', 'light', 'shadow')
    max_num = 3


class SourceAdmin(ManyToManyMixin, admin.ModelAdmin):
    inlines = [ComposingSourceInline]
    m2m_fields = ['cuff_types']


class PlacketAdmin(ManyToManyMixin, admin.ModelAdmin):
    inlines = [ComposingSourceInline]
    m2m_fields = ['plackets']


class CollarSourceAdmin(SourceAdmin):
    inlines = [ComposingSourceInline, CollarMaskInline]


class ButtonsComposingSourceInline(GenericTabularInline):
    model = models.ButtonsSource
    fields = ('projection', 'image', 'ao')
    max_num = 3
    extra = 0


class StitchesSourceInline(GenericTabularInline):
    model = models.StitchesSource
    fields = ('projection', 'type', 'image')
    max_num = 6
    extra = 0


class ButtonsSourceAdmin(admin.ModelAdmin):
    inlines = [ButtonsComposingSourceInline, StitchesSourceInline]

    def get_list_display(self, request):
        return self.get_fields(request)


class CuffButtonsAdmin(ManyToManyMixin, ButtonsSourceAdmin):
    exclude = ['sex']
    m2m_fields = ['rounding_types']


class CuffMaskInline(admin.TabularInline):
    model = models.CuffMask
    fields = ('projection', 'mask', 'element')
    extra = 1
    max_num = 6


class CuffSourceAdmin(SourceAdmin):
    inlines = [ComposingSourceInline, CuffMaskInline]


class TextureAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'needs_shadow', 'thumbnail']
    search_fields = ('texture',)

    thumbnail = AdminThumbnail(image_field='sample', template='processing/sample.html')
    thumbnail.short_description = _(u'Лоскут')


class StitchColorAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'element')
    list_select_related = ('content_type', 'element')


class InitialsPositionInline(admin.TabularInline):
    model = models.InitialsPosition
    extra = 1
    max_num = 3


class InitialsConfigurationAdmin(admin.ModelAdmin):
    model = models.InitialsConfiguration
    list_display = ('font', 'font_size', 'location')
    exclude = ['sex']
    inlines = [InitialsPositionInline]


admin.site.register(models.Texture, TextureAdmin)
admin.site.register(models.StitchColor, StitchColorAdmin)
