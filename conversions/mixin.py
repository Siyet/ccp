# coding: utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from openpyxl import Workbook
from StringIO import StringIO

from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from django.utils.text import ugettext_lazy as _
from import_export.formats.base_formats import XLSX

from backend.models import ElementStitch, ContrastDetails
from core.utils import achain


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

    def get_address_data(self, address):
        return [
            (_(u'Фамилия'), address.lastname, ),
            (_(u'Имя'), address.name, ),
            (_(u'Отчество'), address.midname, ),
            (_(u'Город'), address.city, ),
            (_(u'Адрес'), address.address, ),
            (_(u'Индекс'), address.index, ),
            (_(u'Телефон'), address.phone, ),
            (_(u'E-mail'), address.email, ),
        ]

    def get_delivery(self, instance):
        if instance.checkout_shop:
            return [
                (_(u'Фамилия'), '-', ),
                (_(u'Имя'), '-', ),
                (_(u'Отчество'), '-', ),
                (_(u'Город'), instance.checkout_shop.city, ),
                (_(u'Адрес'), u'%s, %s' % (instance.checkout_shop.street, instance.checkout_shop.home), ),
                (_(u'Индекс'), instance.checkout_shop.index, ),
                (_(u'Телефон'), '-', ),
                (_(u'E-mail'), '-', ),
            ]
        other_address = instance.get_other_address()
        customer_address = instance.get_customer_address()
        address = other_address or customer_address
        return self.get_address_data(address)

    def get_shirt_data(self, shirt):
        data = [[
            _(u'СОРОЧКА'), [
                (_(u'Размер'), shirt.size.size if shirt.size else ''),
                (_(u'Талия'), shirt.get_fit_display() if shirt.fit else ''),
                (_(u'Длина рукава'), shirt.get_sleeve_length_display() if shirt.sleeve_length else ''),
            ]
        ]]
        try:
            data.append(
                [_(u'ВОРОТНИК'), [
                    (_(u'Тип'), shirt.collar.type.title),
                    (_(u'Размер'), shirt.collar.size.title),
                    (_(u'Жесткость воротника'), shirt.collar.hardness.title),
                    (_(u'Косточки'), shirt.collar.stays.title),
                ]]
            )
        except ObjectDoesNotExist:
            pass
        try:
            data.append(
                [_(u'МАНЖЕТЫ'), [
                    (_(u'Тип'), shirt.cuff.type.title),
                    (_(u'Углы'), achain(shirt, 'N/A', 'cuff', 'rounding', 'title')),
                    (_(u'Жесткость манжета'), shirt.cuff.hardness.title),
                    (_(u'Планка рукава'), 'N/A'),
                    (_(u'Складки на рукаве'), 'N/A'),
                    (_(u'Рукав'), 'N/A'),
                ]]
            )
        except ObjectDoesNotExist:
            pass
        try:
            data.append(
                [_(u'ТКАНЬ'), [
                    (_(u'Ткань'), shirt.fabric.code),
                    (_(u'Категория'), shirt.fabric.category.title),
                ]]
            )
        except ObjectDoesNotExist:
            pass
        data.append(
            [_(u'ДЕТАЛИ 1'), [
                (_(u'Низ'), achain(shirt, 'N/A', 'hem', 'title')),
                (_(u'Полочка'), achain(shirt, 'N/A', 'placket', 'title')),
                (_(u'Карман'), achain(shirt, 'N/A', 'pocket', 'title')),
                (_(u'Вытачки'), shirt.get_tuck_display()),
                (_(u'Спинка'), achain(shirt, 'N/A', 'back', 'title')),
                (_(u'Пуговицы'), achain(shirt, 'N/A', 'custom_buttons', 'title')),
            ]]
        )
        if shirt.initials:
            data.append(
                [_(u'ИНИЦИАЛЫ'), [
                    (_(u'Текст'), shirt.initials.text),
                    (_(u'Шрифт'), achain(shirt.initials, 'N/A', 'font', 'title')),
                    (_(u'Цвет'), achain(shirt.initials, 'N/A', 'color', 'title')),
                    (_(u'Расположение'), shirt.initials.get_location_display()),
                ]]
            )

        contrast_stitches = {x.element.title: x.color.title for x in shirt.contrast_stitches.all()}
        detail_rows = []
        for element in ElementStitch.objects.filter(collections=shirt.collection):
            detail_rows.append((element.title, contrast_stitches.get(element.title, '-')))
        detail_rows += [
            (_(u'Платок'), achain(shirt, u'Нет', 'shawl', 'title')),
            (_(u'Цельная кокетка'), achain(shirt, u'Нет', 'yoke', 'title')),
            (_(u'Застежка под штифты'), shirt.get_clasp_display()),
            (_(u'Отстрочка (воротник и манжеты)'), shirt.get_stitch_display()),
        ]
        data.append([_(u'ДЕТАЛИ 2'), detail_rows])

        contrast_details = {x.element: x.fabric.code for x in shirt.contrast_details.all()}
        contrast_detail_rows = [(_(u'Воротник'), '-',)]
        for element in ContrastDetails.COLLAR_ELEMENTS:
            contrast_detail_rows.append((element[1], contrast_details.get(element[0], '-')))
        contrast_detail_rows.append((_(u'Манжета'), '-',))
        for element in ContrastDetails.CUFF_ELEMENTS:
            contrast_detail_rows.append((element[1], contrast_details.get(element[0], '-')))
        data.append([_(u'КОНТРАСТНЫЕ ДЕТАЛИ'), contrast_detail_rows])
        return data

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
        for line in self.get_address_data(order.get_customer_address()):
            ws.append(map(unicode, line))

        # ws.append([u'%s' % _(u'СОРОЧКА'), order.number])
        for cat in self.get_shirt_data(shirt.shirt):
            ws.append([unicode(cat[0])])
            for line in cat[1]:
                ws.append(map(unicode, line))

        ws.append([u'%s' % _(u'ДОСТАВКА')])
        for line in self.get_delivery(order):
            ws.append(map(unicode, line))

        export_data = StringIO()
        wb.save(export_data)
        response = HttpResponse(export_data.getvalue(), content_type=XLSX.CONTENT_TYPE)
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % self.get_export_shirt_filename()
        return response
