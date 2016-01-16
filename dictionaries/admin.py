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

)


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
    DickeyType
])
