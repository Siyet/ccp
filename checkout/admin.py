# coding: utf-8
from __future__ import absolute_import

import datetime
from StringIO import StringIO

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.http.response import Http404
from import_export.formats.base_formats import XLSX
from openpyxl import Workbook
from django.utils.text import ugettext_lazy as _
from import_export.admin import ImportExportMixin

from conversions.mixin import TemplateAndFormatMixin
from conversions.resources import CertificateResource, DiscountResource
from grappelli_orderable.admin import GrappelliOrderableAdmin
from yandex_kassa.admin import Payment as YandexPayment, PaymentAdmin
from .models import (
    Shop,
    Certificate,
    Order,
    OrderDetails,
    Discount,
    CustomerData,
    Payment
)


class CertificateAdmin(TemplateAndFormatMixin, ImportExportMixin, admin.ModelAdmin):
    search_fields = ('number', )
    resource_class = CertificateResource

    def get_export_filename(self, file_format):
        date_str = datetime.datetime.now().strftime('%d_%m_%Y')
        filename = "Certificates_CC_%s.%s" % (date_str, file_format.get_extension())
        return filename


class DiscountAdmin(TemplateAndFormatMixin, ImportExportMixin, admin.ModelAdmin):
    list_display = ('customer', 'discount_value', )
    skip_admin_log = True
    search_fields = ('customer__number', )
    resource_class = DiscountResource
    list_select_related = ('customer',)

    def get_export_filename(self, file_format):
        date_str = datetime.datetime.now().strftime('%d_%m_%Y')
        filename = "Discounts_CC_%s.%s" % (date_str, file_format.get_extension())
        return filename


class ShopAdmin(GrappelliOrderableAdmin):
    list_display = ('city', 'street', 'home')


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 0
    readonly_fields = ('shirt', 'amount', 'get_export_url', )

    def get_export_url(self, instance):
        return u'<a href="export/{}">{}</a>'.format(instance.pk, _(u'Экспорт'))
    get_export_url.allow_tags = True
    get_export_url.short_description = _(u'Экспорт')


class CustomerDataInline(admin.StackedInline):
    model = CustomerData
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'state', 'date_add', 'get_fio', 'get_city', 'get_count', 'get_amount_to_pay',
                    'get_print_url', 'get_export_url', )
    search_fields = ('number', 'customer_data__lastname', 'customer_data__name', 'customer_data__midname',
                     'customer_data__city', 'checkout_shop__city', )
    list_filter = ('state', 'date_add', )
    list_select_related = ('checkout_shop', )
    list_prefetch_related = ('customer_data', 'order_details', )
    readonly_fields = ('date_add', 'get_full_amount', 'get_amount_to_pay', 'get_amount_paid',
                       'get_performed_datetime', )
    inlines = [CustomerDataInline, OrderDetailsInline]

    def get_urls(self):
        urls = super(OrderAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/export/(?P<shirt>\d+)/$', self.admin_site.admin_view(self.export_shirt_action)),
        ]
        return my_urls + urls

    def get_export_shirt_filename(self):
        return 'Orderform_single_shirt'

    def export_shirt_action(self, request, *args, **kwargs):
        order = self.get_object(request, kwargs.get('pk'))
        if not order:
            raise Http404
        shirt = order.get_shirt(kwargs.get('shirt'))
        if not shirt:
            raise Http404
        wb = Workbook()
        ws = wb.active

        ws.append([u'%s' % _(u'Номер заказа'), order.number])
        number = 1
        for ind, x in enumerate(order.order_details.all()):
            if x.pk == shirt.pk:
                number = ind + 1
                break
        ws.append([u'%s' % _(u'Позиция в заказе'), '#%i' % number])

        ws.append([u'%s' % _(u'ДАННЫЕ'), order.number])
        customer_address = order.get_customer_address()
        for line in customer_address.get_data():
            ws.append(line)

        ws.append([u'%s' % _(u'СОРОЧКА'), order.number])
        for cat in shirt.get_data():
            ws.append([cat[0]])
            for line in cat[1]:
                ws.append(line)

        other_address = order.get_other_address()
        delivery = (other_address or customer_address).get_data()
        if order.checkout_shop:
            delivery = order.get_delivery()
        ws.append([u'%s' % _(u'ДОСТАВКА')])
        for line in delivery:
            ws.append(line)

        export_data = StringIO()
        wb.save(export_data)
        response = HttpResponse(export_data.getvalue(), content_type=XLSX.CONTENT_TYPE)
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % self.get_export_shirt_filename()
        return response

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        return qs.prefetch_related(*self.list_prefetch_related)

    def get_print_url(self, instance):
        # TODO: будет дописана в следующих задачах
        return ''
    get_print_url.allow_tags = True
    get_print_url.short_description = _(u'Распечатать инфо о заказе')

    def get_export_url(self, instance):
        # TODO: будет дописана в следующих задачах
        return ''
    get_export_url.allow_tags = True
    get_export_url.short_description = _(u'Сохранить инфо о заказе')


admin.site.register(Order, OrderAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Payment, PaymentAdmin)

admin.site.unregister(YandexPayment)
