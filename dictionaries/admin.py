from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from dictionaries import models
from dictionaries.forms import DefaultElementAdminForm
from grappelli_orderable.admin import GrappelliOrderableAdmin



class SizeAdmin(GrappelliOrderableAdmin):
    list_display = ('size',)


class DefaultElementAdmin(admin.ModelAdmin):
    form = DefaultElementAdminForm


class OrderableTranslationAdmin(GrappelliOrderableAdmin, TranslationAdmin):
    pass

# regular models

admin.site.register(models.DefaultElement, DefaultElementAdmin)

admin.site.register([
    models.Font,
    models.FabricCategory
])

admin.site.register(models.Size, SizeAdmin)

admin.site.register([
    models.Color,
    models.StitchColor,
    models.CollarType
], GrappelliOrderableAdmin)

# translated models

admin.site.register([
    models.TuckType,
    models.CuffRounding,
    models.PocketType,
    models.DickeyType,
    models.HemType,
    models.PlacketType,
    models.CustomButtonsType,
    models.SleeveType,
    models.BackType,
], TranslationAdmin)

admin.site.register([
    models.SizeOptions,
    models.YokeType,
    models.CollarButtons,
    models.FabricDesign,
    models.FabricColor,
    models.CuffType,
    models.FabricType,
    models.Thickness
], OrderableTranslationAdmin)
