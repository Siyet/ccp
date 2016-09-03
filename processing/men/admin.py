# coding: utf-8
from django.contrib import admin
from processing.admin import CollarSourceAdmin, PlacketAdmin, ButtonsSourceAdmin, SourceAdmin, InitialsConfigurationAdmin, CuffSourceAdmin
import models


admin.site.register(models.ManBodyConfiguration, SourceAdmin)
admin.site.register(models.ManCollarConfiguration, CollarSourceAdmin)
admin.site.register(models.ManCuffConfiguration, CuffSourceAdmin)
admin.site.register(models.ManBackConfiguration, SourceAdmin)
admin.site.register(models.ManPocketConfiguration, SourceAdmin)
admin.site.register(models.ManPlacketConfiguration, PlacketAdmin)
admin.site.register(models.ManYokeConfiguration, SourceAdmin)
admin.site.register(models.DickeyConfiguration, SourceAdmin)
admin.site.register(models.ManBodyButtonsConfiguration, ButtonsSourceAdmin)
admin.site.register(models.ManCuffButtonsConfiguration, ButtonsSourceAdmin)
admin.site.register(models.ManInitialsConfiguration, InitialsConfigurationAdmin)
admin.site.register(models.ManCollarButtonsConfiguration, ButtonsSourceAdmin)
