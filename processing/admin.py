# coding: utf-8

from django.contrib import admin
from imagekit.admin import AdminThumbnail
from django.utils.text import ugettext_lazy as _
from django.contrib.contenttypes.admin import GenericTabularInline

import models
from core.admin import ManyToManyMixin


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
