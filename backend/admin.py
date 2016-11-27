# coding: utf-8
from __future__ import absolute_import

import json

from django.conf.urls import url
from django.contrib import admin
from django.http.response import HttpResponse
from django.utils.text import ugettext_lazy as _
from imagekit.admin import AdminThumbnail
from import_export.admin import ImportExportMixin

from conversions.mixin import TemplateAndFormatMixin
from conversions.resources import FabricResidualResource, FabricResource, TemplateShirtResource
from core.admin import ManyToManyMixin
from core.utils import first
from grappelli_orderable.admin import GrappelliOrderableAdmin
from .forms import AccessoriesPriceAdminForm, CuffInlineForm
from .models import *


class ShirtImageInline(admin.TabularInline):
    model = ShirtImage
    extra = 1


class CuffInline(admin.StackedInline):
    model = Cuff
    inline_classes = ('grp-open',)
    form = CuffInlineForm


class CollarInline(admin.StackedInline):
    model = Collar
    inline_classes = ('grp-open',)


class ContrastDetailsInline(admin.TabularInline):
    model = ContrastDetails
    extra = 1
    raw_id_fields = ['fabric']
    autocomplete_lookup_fields = {
        'fk': ['fabric']
    }


class ContrastStitchInline(admin.TabularInline):
    model = ContrastStitch
    extra = 1


class BaseShirtAdmin(GrappelliOrderableAdmin):
    class Media:
        js = ('backend/admin/shirt/scripts.js',)

    def get_urls(self):
        urls = super(BaseShirtAdmin, self).get_urls()
        return [
                   url(r'^[0-9]+/show_cuffs/(?P<pk>[0-9]+)/$', self.show_cuffs),
               ] + urls

    def show_cuffs(self, request, pk):
        try:
            sleeve = SleeveType.objects.get(pk=pk)
            show_cuffs = sleeve.cuffs
        except:
            show_cuffs = True
        return HttpResponse(json.dumps(show_cuffs))

    raw_id_fields = ['fabric']
    autocomplete_lookup_fields = {
        'fk': ['fabric']
    }


class DickeyInline(admin.StackedInline):
    model = Dickey
    inline_classes = ('grp-open',)
    extra = 0
    max_num = 1


class InitialsInline(admin.StackedInline):
    model = Initials
    inline_classes = ('grp-open',)
    extra = 0
    max_num = 1


class CustomShirtAdmin(admin.ModelAdmin):
    inlines = [CollarInline, CuffInline, DickeyInline, ContrastDetailsInline, ContrastStitchInline, InitialsInline]
    exclude = ['is_template', 'code', 'showcase_image', 'individualization']


class TemplateShirtAdmin(TemplateAndFormatMixin, ImportExportMixin, BaseShirtAdmin):
    resource_class = TemplateShirtResource
    exclude = ['is_template']
    inlines = [CollarInline, CuffInline, DickeyInline, ContrastDetailsInline, ContrastStitchInline, InitialsInline,
               ShirtImageInline]
    readonly_fields = ('price',)
    list_select_related = ('hem', 'placket', 'pocket', 'cuff__type', 'collar__type', 'dickey__type', 'collar__hardness')
    list_display = ('code', 'cuff', 'collar', 'hem', 'placket', 'pocket', 'dickey')


class StandardShirtAdmin(admin.ModelAdmin):
    exclude = ['is_template', 'code', 'individualization', 'fabric']


class FabricPriceAdmin(admin.ModelAdmin):
    list_display = ['fabric_category', 'storehouse', 'price']
    list_display_links = ['price']

    def get_queryset(self, request):
        queryset = super(FabricPriceAdmin, self).get_queryset(request)
        return queryset.select_related('fabric_category', 'storehouse')


class FabricResidualAdmin(TemplateAndFormatMixin, ImportExportMixin, admin.ModelAdmin):
    resource_class = FabricResidualResource
    list_select_related = ('fabric', 'storehouse',)
    list_display = ('fabric', 'storehouse', 'amount')

    def get_export_queryset(self, request):
        """
        return all data to export
        """
        qs = self.resource_class._meta.model.objects.all()
        if self.list_select_related:
            qs = qs.select_related(*self.list_select_related)
        return qs


class FabricResidualAdminInline(admin.TabularInline):
    model = FabricResidual
    extra = 0


class FabricAdmin(TemplateAndFormatMixin, ImportExportMixin, admin.ModelAdmin):
    RESIDUAL_KEY = "storehouse_%s"
    list_per_page = 20
    resource_class = FabricResource
    search_fields = ('code',)
    list_filter = ('category',)
    readonly_fields = ['category']
    inlines = [FabricResidualAdminInline, ]
    list_select_related = ('category', 'type', 'thickness', 'texture')

    def __init__(self, *args, **kwargs):
        super(FabricAdmin, self).__init__(*args, **kwargs)
        self.storehouses = Storehouse.objects.all()
        self.bind_storehouse_residuals()

    def bind_storehouse_residuals(self):
        """
        Attaches callable properties to admin class for every fetched storehouse which are resolved to corresponding
        residuals during display cycle
        """
        for storehouse in self.storehouses:
            residual_for_storehouse = lambda self, fabric, storehouse=storehouse: self.get_residual(fabric, storehouse)
            residual_for_storehouse.short_description = storehouse.country
            setattr(FabricAdmin, self.RESIDUAL_KEY % storehouse.id, residual_for_storehouse)

    def get_queryset(self, request):
        queryset = super(FabricAdmin, self).get_queryset(request)
        return queryset.prefetch_related('residuals__storehouse', 'colors', 'designs')

    def get_residual(self, fabric, storehouse):
        residual_predicate = lambda residual: residual.storehouse == storehouse
        residual = first(residual_predicate, fabric.residuals.all())
        return residual.amount if residual else None

    def get_list_display(self, request):
        residual_fields = map(lambda storehouse: self.RESIDUAL_KEY % storehouse.id, self.storehouses)
        list_display = ['code', 'category'] + residual_fields + ['material', 'has_description', 'type',
                                                                 'thickness', 'get_colors', 'get_designs', 'thumbnail']
        return list_display

    def get_list_display_links(self, request, list_display):
        return ('code',)

    # fields
    thumbnail = AdminThumbnail(image_field="get_sample", template='processing/sample.html')
    thumbnail.short_description = _(u'Лоскут')

    def has_description(self, fabric):
        return not (not (fabric.short_description or fabric.long_description))

    has_description.short_description = _(u'Описание')
    has_description.boolean = True

    def get_colors(self, fabric):
        return "; ".join([unicode(color) for color in fabric.colors.all()])

    get_colors.short_description = _(u'Цвета')

    def get_designs(self, fabric):
        return "; ".join([unicode(design) for design in fabric.designs.all()])

    get_designs.short_description = _(u'Дизайн')


class AccessoriesPriceAdmin(admin.ModelAdmin):
    list_display = ('content_type_title', 'price',)
    list_display_links = ('content_type_title', 'price',)
    form = AccessoriesPriceAdminForm


class CollectionAdmin(GrappelliOrderableAdmin):
    list_display = ('title', 'sex')

    class Media:
        js = ('backend/admin/collection/scripts.js',)


class CustomButtonsAdmin(GrappelliOrderableAdmin):
    list_display = ('title', 'type')


class FitAdmin(ManyToManyMixin, GrappelliOrderableAdmin):
    m2m_fields = ['collections']
    exclude = ['sizes', 'picture']


admin.site.register([
    Storehouse,
    ElementStitch
])

admin.site.register(Fit, FitAdmin)

admin.site.register([Hardness, ShawlOptions, Stays], GrappelliOrderableAdmin)

admin.site.register(CustomButtons, CustomButtonsAdmin)

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Fabric, FabricAdmin)
admin.site.register(FabricPrice, FabricPriceAdmin)
admin.site.register(FabricResidual, FabricResidualAdmin)
admin.site.register(CustomShirt, CustomShirtAdmin)
admin.site.register(TemplateShirt, TemplateShirtAdmin)
admin.site.register(AccessoriesPrice, AccessoriesPriceAdmin)
