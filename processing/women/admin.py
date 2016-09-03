# coding: utf-8
from django.contrib import admin
from processing.admin import CollarSourceAdmin, PlacketAdmin, ButtonsSourceAdmin, SourceAdmin, InitialsConfigurationAdmin, CuffButtonsAdmin
import models


# admin.site.register(models.WomanBodyConfiguration, SourceAdmin)
admin.site.register(models.WomanCollarConfiguration, CollarSourceAdmin)
admin.site.register(models.WomanCuffConfiguration, CuffButtonsAdmin)
admin.site.register(models.WomanPocketConfiguration, SourceAdmin)
admin.site.register(models.WomanPlacketConfiguration, PlacketAdmin)
admin.site.register(models.WomanYokeConfiguration, SourceAdmin)
admin.site.register(models.WomanBodyButtonsConfiguration, ButtonsSourceAdmin)
admin.site.register(models.WomanCuffButtonsConfiguration, ButtonsSourceAdmin)
admin.site.register(models.WomanInitialsConfiguration, InitialsConfigurationAdmin)
admin.site.register(models.WomanCollarButtonsConfiguration, ButtonsSourceAdmin)
