# coding: utf-8
import datetime
from django.conf import settings
from django.contrib import admin
from import_export.admin import ImportExportMixin

from checkout.resources import CertificateResource
from .models import (
    Shop,
    Certificate,
    Order,
    OrderDetails,
    OrderAddress,
)


class CertificateAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ('number', )
    resource_class = CertificateResource
    change_list_template = 'admin/backend/change_list_import_export.html'
    import_template_name = 'admin/backend/import.html'
    formats = settings.IMPORT_EXPORT_FORMATS

    def get_export_filename(self, file_format):
        date_str = datetime.datetime.now().strftime('%d_%m_%Y')
        filename = "Certificates_CC_%s.%s" % (date_str, file_format.get_extension())
        return filename


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 0


class OrderAddressInline(admin.TabularInline):
    model = OrderAddress
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailsInline, OrderAddressInline]


admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register([
    Shop,
])