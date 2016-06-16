# coding: utf-8
from __future__ import absolute_import

import datetime
from django.conf import settings
from django.contrib import admin
from import_export.admin import ImportExportMixin

from checkout.import_export.resources import CertificateResource, DiscountResource
from .models import (
    Shop,
    Certificate,
    Discount,
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


class DiscountAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ('customer__number', )
    resource_class = DiscountResource
    change_list_template = 'admin/backend/change_list_import_export.html'
    import_template_name = 'admin/backend/import.html'
    formats = settings.IMPORT_EXPORT_FORMATS

    def get_export_filename(self, file_format):
        date_str = datetime.datetime.now().strftime('%d_%m_%Y')
        filename = "Discounts_CC_%s.%s" % (date_str, file_format.get_extension())
        return filename


admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register([
    Shop,
])