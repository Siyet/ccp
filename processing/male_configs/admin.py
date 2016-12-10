# coding: utf-8
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

import models
from processing.admin import CollarSourceAdmin, PlacketAdmin, ButtonsSourceAdmin, SourceAdmin, \
    InitialsConfigurationAdmin, CuffSourceAdmin, ManyToManyMixin, CuffButtonsAdmin


class BodySourceInline(GenericTabularInline):
    model = models.MaleBodySource
    max_num = 12
    extra = 0
    fields = ('projection', 'tuck', 'uv', 'ao', 'light', 'shadow')


class BodyAdmin(ManyToManyMixin, admin.ModelAdmin):
    inlines = [BodySourceInline]
    m2m_fields = ['cuff_types']



admin.site.register(models.MaleBodyConfiguration, BodyAdmin)
admin.site.register(models.MaleCollarConfiguration, CollarSourceAdmin)
admin.site.register(models.MaleCuffConfiguration, CuffSourceAdmin)
admin.site.register(models.MaleBackConfiguration, SourceAdmin)
admin.site.register(models.MalePocketConfiguration, SourceAdmin)
admin.site.register(models.MalePlacketConfiguration, PlacketAdmin)
admin.site.register(models.MaleYokeConfiguration, SourceAdmin)
admin.site.register(models.DickeyConfiguration, SourceAdmin)
admin.site.register(models.MaleBodyButtonsConfiguration, ButtonsSourceAdmin)
admin.site.register(models.MaleCuffButtonsConfiguration, CuffButtonsAdmin)
admin.site.register(models.MaleInitialsConfiguration, InitialsConfigurationAdmin)
admin.site.register(models.MaleCollarButtonsConfiguration, ButtonsSourceAdmin)
