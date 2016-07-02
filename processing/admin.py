# coding: utf-8

from django.contrib import admin
from imagekit.admin import AdminThumbnail
from django.utils.text import ugettext_lazy as _
import models
from django.contrib.contenttypes.admin import GenericTabularInline


class CollarMaskInline(admin.TabularInline):
    model = models.CollarMask
    max_num = 12
    fields = ('projection', 'mask', 'element')


class ComposingSourceInline(GenericTabularInline):
    model = models.ComposeSource
    fields = ('projection', 'uv', 'ao', 'light')
    max_num = 3


class SourceAdmin(admin.ModelAdmin):
    inlines = [ComposingSourceInline]

    def get_list_display(self, request):
        return self.get_fields(request)


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


class CuffMaskInline(admin.TabularInline):
    model = models.CuffMask
    fields = ('projection', 'mask', 'element')
    extra = 1
    max_num = 6


class CuffMaskSourceAdmin(admin.ModelAdmin):
    inlines = [CuffMaskInline]


class TextureAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'thumbnail']

    thumbnail = AdminThumbnail(image_field='sample', template='processing/sample.html')
    thumbnail.short_description = _(u'Лоскут')


admin.site.register(models.BodySource, SourceAdmin)
admin.site.register(models.CollarSource, CollarSourceAdmin)
admin.site.register(models.CuffSource, SourceAdmin)
admin.site.register(models.CuffMaskSource, CuffMaskSourceAdmin)
admin.site.register(models.BackSource, SourceAdmin)
admin.site.register(models.PocketSource, SourceAdmin)
admin.site.register(models.PlacketSource, SourceAdmin)
admin.site.register(models.BodyButtonsSource, ButtonsSourceAdmin)
admin.site.register(models.CollarButtonsSource, ButtonsSourceAdmin)
admin.site.register(models.CuffButtonsSource, ButtonsSourceAdmin)
admin.site.register(models.Texture, TextureAdmin)