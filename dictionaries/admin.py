from django.contrib import admin
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
)


class ShirtInfoImageInline(admin.TabularInline):
    model = ShirtInfoImage
    extra = 0


class ShirtInfoAdmin(admin.ModelAdmin):
    inlines = [ShirtInfoImageInline]


class SizeAdmin(GrappelliOrderableAdmin):
    list_display = ('size',)


admin.site.register(ShirtInfo, ShirtInfoAdmin)
admin.site.register([
    Color,
    Font,
    FabricColor,
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
])

admin.site.register(Size, SizeAdmin)

admin.site.register([SizeOptions, FabricDesign, CollarButtons, CollarType, CuffType, FabricType, Thickness],
                    GrappelliOrderableAdmin)