from django.contrib import admin

from .models import (
    Color,
    FabricColor,
    FabricDesign,
    FabricCategory,
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
    Size
)


class ShirtInfoImageInline(admin.TabularInline):
    model = ShirtInfoImage
    extra = 0


class ShirtInfoAdmin(admin.ModelAdmin):
    inlines = [ShirtInfoImageInline]


admin.site.register(ShirtInfo, ShirtInfoAdmin)
admin.site.register([
    Color,
    FabricColor,
    FabricDesign,
    FabricCategory,
    CollarButtons,

    CollarType,
    CuffRounding,
    CuffType,
    CustomButtonsType,
    YokeType,
    StitchColor,
    DickeyType,
    SizeOptions,
    Size
])
