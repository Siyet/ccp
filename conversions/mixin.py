# coding: utf-8
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.http import HttpResponse
from django.utils.text import ugettext_lazy as _

from backend.models import ElementStitch, ContrastDetails
from core.utils import achain

EMPTY = '---'
EMPTY_ROW = ''

class TemplateAndFormatMixin(object):
    formats = settings.IMPORT_EXPORT_FORMATS
    change_list_template = 'admin/conversions/change_list_import_export.html'
    import_template_name = 'admin/conversions/import.html'


class OrderExportMixin(object):

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
            EMPTY_ROW
        ]

    def get_delivery(self, instance):

        if instance.checkout_shop:
            return [
                (_(u'Фамилия'), EMPTY, ),
                (_(u'Имя'), EMPTY, ),
                (_(u'Отчество'), EMPTY, ),
                (_(u'Город'), instance.checkout_shop.city, ),
                (_(u'Адрес'), u'%s, %s' % (instance.checkout_shop.street, instance.checkout_shop.home), ),
                (_(u'Индекс'), instance.checkout_shop.index, ),
                (_(u'Телефон'), EMPTY, ),
                (_(u'E-mail'), EMPTY, ),
                EMPTY_ROW
            ]
        other_address = instance.get_other_address()
        customer_address = instance.get_customer_address()
        address = other_address or customer_address
        return self.get_address_data(address)

    def get_shirt_data(self, shirt):
        data = [[
            _(u'СОРОЧКА'), [
                (_(u'Коллекция'), shirt.collection, ),
                (_(u'Размер'), shirt.size.size if shirt.size else EMPTY),
                (_(u'Талия'), shirt.fit.title if shirt.fit else EMPTY),
                EMPTY_ROW
            ]
        ]]
        try:
            data.append(
                [_(u'ВОРОТНИК'), [
                    (_(u'Тип'), shirt.collar.type.title),
                    (_(u'Размер'), shirt.collar.size.title),
                    (_(u'Жесткость воротника'), shirt.collar.hardness.title),
                    (_(u'Косточки'), shirt.collar.stays.title),
                    EMPTY_ROW
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
                    EMPTY_ROW
                ]]
            )
        except ObjectDoesNotExist:
            data.append(
                [_(u'МАНЖЕТЫ'), [
                    (_(u'Тип'), EMPTY),
                    (_(u'Углы'), EMPTY),
                    (_(u'Жесткость манжета'), EMPTY),
                    EMPTY_ROW
                ]]
            )
        try:
            data.append(
                [_(u'ТКАНЬ'), [
                    (_(u'Ткань'), shirt.fabric.code),
                    (_(u'Категория'), shirt.fabric.category.title),
                    EMPTY_ROW
                ]]
            )
        except ObjectDoesNotExist:
            pass
        data.append(
            [_(u'ДЕТАЛИ 1'), [
                (_(u'Низ'), achain(shirt, 'N/A', 'hem', 'title')),
                (_(u'Полочка'), achain(shirt, 'N/A', 'placket', 'title')),
                (_(u'Карман'), achain(shirt, 'N/A', 'pocket', 'title')),
                (_(u'Вытачки'), achain(shirt, 'N/A', 'tuck', 'title')),
                (_(u'Спинка'), achain(shirt, 'N/A', 'back', 'title')),
                (_(u'Пуговицы'), achain(shirt, 'N/A', 'custom_buttons', 'title')),
                EMPTY_ROW
            ]]
        )

        try:
            data.append(
                [_(u'ИНИЦИАЛЫ'), [
                    (_(u'Текст'), shirt.initials.text),
                    (_(u'Шрифт'), achain(shirt.initials, 'N/A', 'font', 'title')),
                    (_(u'Цвет'), achain(shirt.initials, 'N/A', 'color', 'title')),
                    (_(u'Расположение'), shirt.initials.get_location_display()),
                    EMPTY_ROW
                ]]
            )
        except ObjectDoesNotExist:
            pass

        contrast_stitches = {x.element.title: x.color.title for x in shirt.contrast_stitches.all()}
        detail_rows = []
        for element in ElementStitch.objects.filter(collections=shirt.collection):
            detail_rows.append((element.title, contrast_stitches.get(element.title, EMPTY)))
        detail_rows += [
            (_(u'Платок'), achain(shirt, _(u'Нет'), 'shawl', 'title')),
            (_(u'Цельная кокетка'), achain(shirt, _(u'Нет'), 'yoke', 'title')),
            (_(u'Застежка под штифты'), shirt.get_clasp_display()),
            (_(u'Отстрочка (воротник и манжеты)'), shirt.get_stitch_display()),
            EMPTY_ROW
        ]
        data.append([_(u'ДЕТАЛИ 2'), detail_rows])

        contrast_details = {x.element: x.fabric.code for x in shirt.contrast_details.all()}
        contrast_detail_rows = [(_(u'Воротник'), EMPTY,)]
        for element in ContrastDetails.COLLAR_ELEMENTS:
            contrast_detail_rows.append((element[1], contrast_details.get(element[0], EMPTY)))
        contrast_detail_rows.append((_(u'Манжета'), EMPTY,))
        for element in ContrastDetails.CUFF_ELEMENTS:
            contrast_detail_rows.append((element[1], contrast_details.get(element[0], EMPTY)))
        data.append([_(u'КОНТРАСТНЫЕ ДЕТАЛИ'), contrast_detail_rows])
        return data

    def get_order_data(self, order):
        data = [
            (_(u'Номер заказа'), order.number),
            (_(u'Общая стоимость заказа'), order.get_amount_to_pay()),
            (_(u'Дата оплаты заказа'), order.get_performed_datetime()),
        ]
        if order.certificate:
            data += [
                (_(u'Использование сертификата'), _(u'Да')),
                (_(u'Номер сертификата'), order.certificate.number),
                (_(u'Номинал сертификата'), u'%s рублей' % order.certificate_value),
            ]
        else:
            data += [
                (_(u'Использование сертификата'), _(u'Нет')),
            ]
        if order.discount_value is not None and order.customer and order.discount_value > 0:
            data += [
                (_(u'Использование скидки'), _(u'Да')),
                (_(u'Номинал скидки'), '%s %%' % (order.customer.get_discount_value() * 100.0)),
                (_(u'Размер скидки'), u'%s рублей' % order.discount_value),
                (_(u'Номер скидочной карты'), order.customer.number),
            ]
        else:
            data += [
                (_(u'Использование скидки'), _(u'Нет')),
            ]
        return data

    def get_shirt_lines(self, order, order_detail, number):
        """
        Get order_detail info to list of string

        Args:
            order: Order model
            order_detail: OrderDetail model
            number: number order_detail in order
        Returns:
            list of string
        """
        lines = [
            [u'%s' % _(u'Номер заказа'), order.number],
            [u'%s' % _(u'Позиция в заказе'), '#%i' % number],
            [EMPTY_ROW],
            [u'%s' % _(u'ДАННЫЕ'), order.number]
        ]
        for line in self.get_address_data(order.get_customer_address()):
            lines.append(map(unicode, line))

        for cat in self.get_shirt_data(order_detail.shirt):
            lines.append([unicode(cat[0])])
            for line in cat[1]:
                lines.append(map(unicode, line))

        lines.append([EMPTY_ROW])
        lines.append([u'%s' % _(u'ДОСТАВКА')])
        for line in self.get_delivery(order):
            lines.append(map(unicode, line))
        return lines

    def get_order_lines(self, order):
        """
        Get order info to list of string
        
        Args:
            order: Order model
        Returns:
            list of string
        """
        lines = [
            [u'%s' % _(u'Заказ')]
        ]
        for line in self.get_order_data(order):
            lines.append(map(unicode, line))

        lines.append([EMPTY_ROW])
        lines.append([u'%s' % _(u'ДАННЫЕ КЛИЕНТА'), order.number])
        for line in self.get_address_data(order.get_customer_address()):
            lines.append(map(unicode, line))

        lines.append([EMPTY_ROW])
        lines.append([u'%s' % _(u'АДРЕС ДОСТАВКИ')])
        for line in self.get_delivery(order):
            lines.append(map(unicode, line))
        return lines
