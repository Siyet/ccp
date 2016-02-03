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
    Shirt,
    ShirtImage
)


class ShirtImageInline(admin.TabularInline):
    model = ShirtImage
    extra = 1


class CuffInline(admin.StackedInline):
    model = Cuff
    inline_classes = ('grp-open',)


class CollarInline(admin.StackedInline):
    model = Collar
    inline_classes = ('grp-open',)


class ShirtAdmin(admin.ModelAdmin):
    inlines = [CollarInline, CuffInline, ShirtImageInline]


class FabricPriceAdmin(admin.ModelAdmin):
    list_display = ['fabric_category', 'storehouse', 'price']
    list_display_links = ['price']

    def get_queryset(self, request):
        queryset = super(FabricPriceAdmin, self).get_queryset(request)
        return queryset.select_related('fabric_category', 'storehouse')


admin.site.register([
    Collection,
    Storehouse,
    Fabric,
    FabricResidual,
    CustomButtons,
    ShawlOptions,
    Dickey,
    Initials,
    ContrastDetails,
    ContrastStitch
])

admin.site.register(FabricPrice, FabricPriceAdmin)
admin.site.register(Shirt, ShirtAdmin)
