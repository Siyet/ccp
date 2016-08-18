# coding: utf-8
from StringIO import StringIO

from openpyxl import Workbook
from django.utils.text import ugettext_lazy as _

from .mixin import OrderExportMixin


class OrderDetailReportGenerator(OrderExportMixin):

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