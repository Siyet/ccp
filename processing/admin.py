# coding: utf-8

from django.contrib import admin
from imagekit.admin import AdminThumbnail
from django.utils.text import ugettext_lazy as _
from django.contrib.contenttypes.admin import GenericTabularInline

import models


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
            m2m_field = next(f for f in self.model._meta.many_to_many if f.name == field_name)
            formatter = ManyToManyListFormatter(field_name, m2m_field.verbose_name)

            field_attr = list_display[field_idx] + "_list"
            list_display[field_idx] = field_attr
            setattr(self, field_attr, formatter)
        return list_display

    def get_queryset(self, request):
        fields = self.get_fields(request)
        prefetch_fields = filter(lambda f: f in fields, self.m2m_fields)
        return super(ManyToManyMixin, self).get_queryset(request).prefetch_related(*prefetch_fields)


class CollarMaskInline(admin.TabularInline):
    model = models.CollarMask
    max_num = 12
    fields = ('projection', 'mask', 'element')


class ComposingSourceInline(GenericTabularInline):
    model = models.ComposeSource
    fields = ('projection', 'uv', 'ao', 'light')
    max_num = 3


class SourceAdmin(ManyToManyMixin, admin.ModelAdmin):
    inlines = [ComposingSourceInline]
    m2m_fields = ['cuff_types']


class CollarSourceAdmin(SourceAdmin):
    inlines = [ComposingSourceInline, CollarMaskInline]


class ButtonsComposingSourceInline(GenericTabularInline):
    model = models.ButtonsSource
    fields = ('projection', 'image', 'ao')
    max_num = 3


class ButtonsSourceAdmin(admin.ModelAdmin):
    inlines = [ButtonsComposingSourceInline]

    def get_list_display(self, request):
        return self.get_fields(request)


class CuffButtonsAdmin(ManyToManyMixin, ButtonsSourceAdmin):
    inlines = [ButtonsComposingSourceInline]
    m2m_fields = ['rounding_types']


class CuffMaskInline(admin.TabularInline):
    model = models.CuffMask
    fields = ('projection', 'mask', 'element')
    extra = 1
    max_num = 6


class CuffSourceAdmin(SourceAdmin):
    inlines = [ComposingSourceInline, CuffMaskInline]


class TextureAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'thumbnail']

    thumbnail = AdminThumbnail(image_field='sample', template='processing/sample.html')
    thumbnail.short_description = _(u'Лоскут')


admin.site.register(models.BodySource, SourceAdmin)
admin.site.register(models.CollarSource, CollarSourceAdmin)
admin.site.register(models.CuffSource, CuffSourceAdmin)
admin.site.register(models.BackSource, SourceAdmin)
admin.site.register(models.PocketSource, SourceAdmin)
admin.site.register(models.PlacketSource, SourceAdmin)
admin.site.register(models.BodyButtonsSource, ButtonsSourceAdmin)
admin.site.register(models.CollarButtonsSource, ButtonsSourceAdmin)
admin.site.register(models.CuffButtonsSource, CuffButtonsAdmin)
admin.site.register(models.Texture, TextureAdmin)
