# coding: utf-8
from django.contrib import admin
from processing.admin import CollarSourceAdmin, PlacketAdmin, ButtonsSourceAdmin, SourceAdmin, InitialsConfigurationAdmin, CuffSourceAdmin
import models


admin.site.register(models.MaleBodyConfiguration, SourceAdmin)
admin.site.register(models.MaleCollarConfiguration, CollarSourceAdmin)
admin.site.register(models.MaleCuffConfiguration, CuffSourceAdmin)
admin.site.register(models.MaleBackConfiguration, SourceAdmin)
admin.site.register(models.MalePocketConfiguration, SourceAdmin)
admin.site.register(models.MalePlacketConfiguration, PlacketAdmin)
admin.site.register(models.MaleYokeConfiguration, SourceAdmin)
admin.site.register(models.DickeyConfiguration, SourceAdmin)
admin.site.register(models.MaleBodyButtonsConfiguration, ButtonsSourceAdmin)
admin.site.register(models.MaleCuffButtonsConfiguration, ButtonsSourceAdmin)
admin.site.register(models.MaleInitialsConfiguration, InitialsConfigurationAdmin)
admin.site.register(models.MaleCollarButtonsConfiguration, ButtonsSourceAdmin)
