# coding: utf-8
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from processing.admin import CollarSourceAdmin, PlacketAdmin, ButtonsSourceAdmin, SourceAdmin, InitialsConfigurationAdmin, CuffButtonsAdmin, ManyToManyMixin
import models


class BodySourceInline(GenericTabularInline):
    model = models.FemaleBodySource
    max_num = 12
    fields = ('projection', 'back', 'uv', 'ao', 'light')


class BodyAdmin(ManyToManyMixin, admin.ModelAdmin):
    inlines = [BodySourceInline]
    m2m_fields = ['cuff_types']


class CuffsAdmin(SourceAdmin):
    exclude = ['side_mask', 'sex']


admin.site.register(models.FemaleBodyConfiguration, BodyAdmin)
admin.site.register(models.FemaleCollarConfiguration, CollarSourceAdmin)
admin.site.register(models.FemaleCuffConfiguration, CuffsAdmin)
admin.site.register(models.FemalePocketConfiguration, SourceAdmin)
admin.site.register(models.FemalePlacketConfiguration, PlacketAdmin)
admin.site.register(models.FemaleYokeConfiguration, SourceAdmin)
admin.site.register(models.FemaleBodyButtonsConfiguration, ButtonsSourceAdmin)
admin.site.register(models.FemaleCuffButtonsConfiguration, CuffButtonsAdmin)
admin.site.register(models.FemaleInitialsConfiguration, InitialsConfigurationAdmin)
admin.site.register(models.FemaleCollarButtonsConfiguration, ButtonsSourceAdmin)
admin.site.register(models.FemaleBackShadow)
