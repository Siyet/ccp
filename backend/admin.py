# coding: utf-8
from django.contrib import admin
from .models import (
    Collection,
    Storehouse,
    Fabric,
    FabricPrice,
    FabricResidual,
    Collar,
    Cuff,
    CustomButtons,
    ShawlOptions,
    Dickey,
    Initials,
    ContrastDetails,
    ContrastStitch,
    Shirt
)

class CollarAdmin(admin.ModelAdmin):
    list_display = ['type', 'hardness', 'stays']

class CuffAdmin(admin.ModelAdmin):
    list_display = ['type', 'hardness', 'sleeve']

admin.site.register([
    Collection,
    Storehouse,
    Fabric,
    FabricPrice,
    FabricResidual,
    CustomButtons,
    ShawlOptions,
    Dickey,
    Initials,
    ContrastDetails,
    ContrastStitch,
    Shirt
])

admin.site.register(Collar, CollarAdmin)
admin.site.register(Cuff, CuffAdmin)
