# coding: utf-8
from __future__ import absolute_import

import datetime

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.http import HttpResponse
from django.utils.text import ugettext_lazy as _
from import_export.admin import ImportExportMixin

from conversions.mixin import TemplateAndFormatMixin
from conversions.admin import OrderExportAdmin
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
    exclude = ('shirt', )
    readonly_fields = ('get_shirt_url', 'amount', 'price', 'get_export_url', )

    def get_shirt_url(self, instance):
        return u'<a href="{}">{}</a>'.format(
            reverse('admin:backend_customshirt_change', args=(instance.shirt_id, )), _(u'Рубашка')
        )
    get_shirt_url.allow_tags = True
    get_shirt_url.short_description = _(u'Рубашка')

    def get_export_url(self, instance):
        return u'<a href="export/{}">{}</a>'.format(instance.pk, _(u'Экспорт'))
    get_export_url.allow_tags = True
    get_export_url.short_description = _(u'Экспорт')


class CustomerDataInline(admin.StackedInline):
    model = CustomerData
    extra = 0


class OrderAdmin(OrderExportAdmin):
    list_display = ('number', 'state', 'get_payment_status', 'date_add', 'get_fio', 'get_city', 'get_count',
                    'get_amount_to_pay', 'get_print_url', 'get_export_url', )
    search_fields = ('number', 'customer_data__lastname', 'customer_data__name', 'customer_data__midname',
                     'customer_data__city', 'checkout_shop__city', )
    list_filter = ('state', 'date_add', 'payment__status',)
    list_select_related = ('checkout_shop', 'payment', )
    list_prefetch_related = ('customer_data', 'order_details', )
    readonly_fields = ('get_payment_status', 'date_add', 'get_full_amount', 'get_amount_to_pay', 'get_amount_paid',
                       'get_performed_datetime', )
    inlines = [CustomerDataInline, OrderDetailsInline]

    order_pdf_template_name = 'checkout/payment_completed_customer_pdf_email.html'
    CONTENT_TYPE_PDF = 'application/pdf'

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        return qs.prefetch_related(*self.list_prefetch_related)

    def get_urls(self):
        urls = super(OrderAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<pk>\d+)/pdf/$',
                self.admin_site.admin_view(self.pdf_action),
                name='checkout_order_pdf'
            ),
        ]
        return my_urls + urls

    def pdf_action(self, request, *args, **kwargs):
        order = self.get_object(request, kwargs.get('pk'))
        response = HttpResponse(order.get_pdf(), content_type=self.CONTENT_TYPE_PDF)
        response['Content-Disposition'] = 'inline; filename=%s.pdf' % self.get_export_filename()
        return response

    def get_print_url(self, instance):
        return u'<a href="{}">{}</a>'\
            .format(reverse('admin:checkout_order_pdf', args=(instance.pk, )), _(u'PDF'))
    get_print_url.allow_tags = True
    get_print_url.short_description = _(u'Распечатать инфо о заказе')

    def get_export_url(self, instance):
        return u'<a href="{}">{}</a>'\
            .format(reverse('admin:checkout_order_export', args=(instance.pk, )), _(u'Экспорт'))
    get_export_url.allow_tags = True
    get_export_url.short_description = _(u'Сохранить инфо о заказе')



admin.site.register(Order, OrderAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Payment, PaymentAdmin)

admin.site.unregister(YandexPayment)
