# coding: utf-8
from django.http.response import Http404
from openpyxl import Workbook
from StringIO import StringIO

from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from django.utils.text import ugettext_lazy as _
from import_export.formats.base_formats import XLSX


class TemplateAndFormatMixin(object):
    formats = settings.IMPORT_EXPORT_FORMATS
    change_list_template = 'admin/conversions/change_list_import_export.html'
    import_template_name = 'admin/conversions/import.html'


class OrderExportMixin(object):
    def get_urls(self):
        urls = super(OrderExportMixin, self).get_urls()
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
            ws.append(map(unicode, line))

        ws.append([u'%s' % _(u'СОРОЧКА'), order.number])
        for cat in shirt.get_data:
            ws.append([unicode(cat[0])])
            for line in cat[1]:
                ws.append(map(unicode, line))

        other_address = order.get_other_address()
        delivery = (other_address or customer_address).get_data()
        if order.checkout_shop:
            delivery = order.get_delivery()
        ws.append([u'%s' % _(u'ДОСТАВКА')])
        for line in delivery:
            ws.append(map(unicode, line))

        export_data = StringIO()
        wb.save(export_data)
        response = HttpResponse(export_data.getvalue(), content_type=XLSX.CONTENT_TYPE)
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % self.get_export_shirt_filename()
        return response
