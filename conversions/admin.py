# coding: utf-8
from django.conf.urls import url
from django.http.response import HttpResponse, Http404
from import_export.formats.base_formats import XLSX

from .report import OrderDetailReportGenerator
from .archive import ArchiveGenerator


class OrderExportAdmin(object):
    CONTENT_TYPE_ZIP = 'application/zip'
    report_generator_class = OrderDetailReportGenerator
    archive_generator_class = ArchiveGenerator

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
        report_generator = self.report_generator_class()
        xlsx = report_generator.get_shirt_xlsx(order, shirt, number)
        response = HttpResponse(xlsx, content_type=XLSX.CONTENT_TYPE)
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % self.get_export_shirt_filename()
        return response

    def export_action(self, request, *args, **kwargs):
        order = self.get_object(request, kwargs.get('pk'))
        report_generator = self.report_generator_class()
        archive_generator = self.archive_generator_class()
        for ind, shirt in enumerate(order.order_details.all()):
            xlsx = report_generator.get_shirt_xlsx(order, shirt, ind + 1)
            archive_generator.add(
                '%i_%i_%s.xlsx' % (order.pk, ind + 1, self.get_export_shirt_filename()),
                xlsx
            )
        xlsx = report_generator.get_order_xlsx(order)
        archive_generator.add(
            '%i_%s.xlsx' % (order.pk, self.get_export_filename()),
            xlsx
        )
        response = HttpResponse(archive_generator.archive(), content_type=self.CONTENT_TYPE_ZIP)
        response['Content-Disposition'] = 'attachment; filename=%s.zip' % self.get_export_filename()
        return response