from django.contrib import admin

from .models import (
    Color,
    FabricColor,
    FabricDesign,
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
    CollarButtons,
    CollarType,
    CuffRounding,
    CuffType,
    CustomButtonsType,
    YokeType,
    StitchColor,
    DickeyType
])
