# coding: utf-8
from StringIO import StringIO
from zipfile import ZipFile

from django.http.response import Http404
from openpyxl import Workbook

from django.conf.urls import url
from django.http import HttpResponse
from django.utils.text import ugettext_lazy as _
from import_export.formats.base_formats import XLSX

from .mixin import OrderExportMixin


class OrderExportAdmin(OrderExportMixin):
    CONTENT_TYPE_ZIP = 'application/zip'

    def get_urls(self):
        urls = super(OrderExportAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<pk>\d+)/export/$',
                self.admin_site.admin_view(self.export_action),
                name='checkout_order_export'
            ),
            url(r'^(?P<pk>\d+)/export/(?P<shirt>\d+)/$', self.admin_site.admin_view(self.export_shirt_action)),
        ]
        return my_urls + urls

    def get_export_filename(self):
        return 'Order'

    def get_export_shirt_filename(self):
        return 'Orderform_single_shirt'

    def get_shirt_xlsx(self, order, order_detail, number):
        """
        Get OrderDetail XLSX

        Args:
            order: Order object
            order_detail: OrderDetail object
            number: OrderDetail number in Order
        Returns:
            string
        """
        wb = Workbook()
        ws = wb.active

        ws.append([u'%s' % _(u'Номер заказа'), order.number])
        ws.append([u'%s' % _(u'Позиция в заказе'), '#%i' % number])

        ws.append([u'%s' % _(u'ДАННЫЕ'), order.number])
        for line in self.get_address_data(order.get_customer_address()):
            ws.append(map(unicode, line))

        for cat in self.get_shirt_data(order_detail.shirt):
            ws.append([unicode(cat[0])])
            for line in cat[1]:
                ws.append(map(unicode, line))

        ws.append([u'%s' % _(u'ДОСТАВКА')])
        for line in self.get_delivery(order):
            ws.append(map(unicode, line))

        export_data = StringIO()
        wb.save(export_data)
        return export_data.getvalue()

    def get_order_xlsx(self, order):
        """
        Get Order XLSX

        Args:
            order: Order object
        Returns:
            string
        """
        wb = Workbook()
        ws = wb.active
        ws.append([u'%s' % _(u'Заказ')])
        for line in self.get_order_data(order):
            ws.append(map(unicode, line))

        ws.append([u'%s' % _(u'ДАННЫЕ КЛИЕНТА'), order.number])
        for line in self.get_address_data(order.get_customer_address()):
            ws.append(map(unicode, line))

        ws.append([u'%s' % _(u'АДРЕС ДОСТАВКИ')])
        for line in self.get_delivery(order):
            ws.append(map(unicode, line))
        export_data = StringIO()
        wb.save(export_data)
        return export_data.getvalue()

    def export_shirt_action(self, request, *args, **kwargs):
        order = self.get_object(request, kwargs.get('pk'))
        if not order:
            raise Http404
        shirt = order.get_shirt(kwargs.get('shirt'))
        if not shirt:
            raise Http404
        number = 1
        for ind, x in enumerate(order.order_details.all()):
            if x.pk == shirt.pk:
                number = ind + 1
                break
        xlsx = self.get_shirt_xlsx(order, shirt, number)
        response = HttpResponse(xlsx, content_type=XLSX.CONTENT_TYPE)
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % self.get_export_shirt_filename()
        return response

    def export_action(self, request, *args, **kwargs):
        order = self.get_object(request, kwargs.get('pk'))
        fz = StringIO()
        with ZipFile(fz, 'w') as response_zip:
            for ind, shirt in enumerate(order.order_details.all()):
                xlsx = self.get_shirt_xlsx(order, shirt, ind + 1)
                response_zip.writestr('%i_%i_%s.xlsx' % (order.pk, ind + 1, self.get_export_shirt_filename()), xlsx)
            xlsx = self.get_order_xlsx(order)
            response_zip.writestr('%i_%s.xlsx' % (order.pk, self.get_export_filename()), xlsx)
        response = HttpResponse(fz.getvalue(), content_type=self.CONTENT_TYPE_ZIP)
        response['Content-Disposition'] = 'attachment; filename=%s.zip' % self.get_export_filename()
        return response