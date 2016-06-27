# coding: utf-8
from __future__ import absolute_import

import datetime
from django.contrib import admin
from import_export.admin import ImportExportMixin

from backend.import_export.mixin import TemplateAndFormatMixin
from checkout.import_export.resources import CertificateResource, DiscountResource
from grappelli_orderable.admin import GrappelliOrderableAdmin
from .models import (
    Shop,
    Certificate,
    Order,
    OrderDetails,
    OrderAddress,
    Discount,
)


class CertificateAdmin(TemplateAndFormatMixin, ImportExportMixin, admin.ModelAdmin):
    search_fields = ('number', )
    resource_class = CertificateResource

    def get_export_filename(self, file_format):
        date_str = datetime.datetime.now().strftime('%d_%m_%Y')
        filename = "Certificates_CC_%s.%s" % (date_str, file_format.get_extension())
        return filename


class DiscountAdmin(TemplateAndFormatMixin, ImportExportMixin, admin.ModelAdmin):
    search_fields = ('customer__number', )
    resource_class = DiscountResource

    def get_export_filename(self, file_format):
        date_str = datetime.datetime.now().strftime('%d_%m_%Y')
        filename = "Discounts_CC_%s.%s" % (date_str, file_format.get_extension())
        return filename


class ShopAdmin(GrappelliOrderableAdmin):
    list_display = ('city', 'street', 'home')


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 0


class OrderAddressInline(admin.TabularInline):
    model = OrderAddress
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailsInline, OrderAddressInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Shop, ShopAdmin)
