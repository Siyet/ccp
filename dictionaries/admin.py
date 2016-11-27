from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from dictionaries import models
from dictionaries.forms import DefaultElementAdminForm
from grappelli_orderable.admin import GrappelliOrderableAdmin


class ShirtInfoImageInline(admin.TabularInline):
    model = models.ShirtInfoImage
    extra = 0


class ShirtInfoAdmin(admin.ModelAdmin):
    inlines = [ShirtInfoImageInline]


class SizeAdmin(GrappelliOrderableAdmin):
    list_display = ('size',)


class DefaultElementAdmin(admin.ModelAdmin):
    form = DefaultElementAdminForm


class OrderableTranslationAdmin(GrappelliOrderableAdmin, TranslationAdmin):
    pass

# regular models

admin.site.register(models.ShirtInfo, ShirtInfoAdmin)
admin.site.register(models.DefaultElement, DefaultElementAdmin)

admin.site.register([
    models.Font,
    models.FabricCategory,
    models.FAQ
])

admin.site.register(models.Size, SizeAdmin)

admin.site.register([
    models.Color,
    models.StitchColor,
    models.FabricColor,
    models.CollarType
], GrappelliOrderableAdmin)

# translated models

admin.site.register([
    models.TuckType,
    models.SleeveLength,
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
    models.CuffType,
    models.FabricType,
    models.Thickness
], OrderableTranslationAdmin)
