from django.contrib import admin

from dictionaries.forms import DefaultElementAdminForm
from grappelli_orderable.admin import GrappelliOrderableAdmin

from .models import (
    Color,
    Font,
    FabricColor,
    FabricDesign,
    FabricCategory,
    FabricType,
    CollarButtons,
    CollarType,
    CuffRounding,
    CuffType,
    CustomButtonsType,
    YokeType,
    StitchColor,
    DickeyType,
    ShirtInfo,
    ShirtInfoImage,
    SizeOptions,
    Size,
    HemType,
    BackType,
    PlacketType,
    PocketType,
    SleeveType,
    Thickness,
    FAQ,
    SleeveLength,
    DefaultElement,
    TuckType
)


class ShirtInfoImageInline(admin.TabularInline):
    model = ShirtInfoImage
    extra = 0


class ShirtInfoAdmin(admin.ModelAdmin):
    inlines = [ShirtInfoImageInline]


class SizeAdmin(GrappelliOrderableAdmin):
    list_display = ('size',)


class DefaultElementAdmin(admin.ModelAdmin):
    form = DefaultElementAdminForm


admin.site.register(ShirtInfo, ShirtInfoAdmin)
admin.site.register(DefaultElement, DefaultElementAdmin)
admin.site.register([
    Color,
    Font,
    FabricCategory,
    CuffRounding,
    CustomButtonsType,
    YokeType,
    StitchColor,
    DickeyType,
    HemType,
    BackType,
    PlacketType,
    PocketType,
    SleeveType,
    FAQ,
    SleeveLength,
    TuckType
])

admin.site.register(Size, SizeAdmin)

admin.site.register([SizeOptions, FabricColor, FabricDesign, CollarButtons, CollarType, CuffType, FabricType, Thickness],
                    GrappelliOrderableAdmin)