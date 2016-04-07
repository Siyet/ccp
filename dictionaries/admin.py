from django.contrib import admin

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
    HemType, BackType, PlacketType, PocketType, SleeveType
)


class ShirtInfoImageInline(admin.TabularInline):
    model = ShirtInfoImage
    extra = 0


class ShirtInfoAdmin(admin.ModelAdmin):
    inlines = [ShirtInfoImageInline]


admin.site.register(ShirtInfo, ShirtInfoAdmin)
admin.site.register([
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
    SizeOptions,
    Size,
    HemType,
    BackType,
    PlacketType,
    PocketType,
    SleeveType
])
