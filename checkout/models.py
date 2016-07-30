# coding: utf-8
import uuid

from django.db import models
from django.db.transaction import atomic
from django.dispatch.dispatcher import receiver
from django.utils.text import ugettext_lazy as _
from model_utils import Choices

from ordered_model.models import OrderedModel
from yandex_kassa.models import Payment as YandexPayment
from yandex_kassa.signals import payment_completed

from core.mail import CostumecodeMailer
from core.utils import first


class Payment(YandexPayment):
    class Meta:
        proxy = True
        ordering = ('-created', )
        verbose_name = _(u'Платеж')
        verbose_name_plural = _(u'Платежи')


class Customer(models.Model):
    number = models.CharField(_(u'Уникальный номер пользователя'), max_length=255, unique=True)

    def __unicode__(self):
        return self.number

    def get_discount_value(self):
        try:
            return float(self.discount.discount_value)
        except (AttributeError, TypeError):
            return 0

    class Meta:
        verbose_name = _(u'Клиент')
        verbose_name_plural = _(u'Клиенты')


class Shop(OrderedModel):
    index = models.IntegerField(verbose_name=_(u'Индекс'), unique=True)
    city = models.CharField(verbose_name=_(u'Город'), max_length=255)
    street = models.CharField(verbose_name=_(u'Улица'), max_length=255)
    home = models.CharField(verbose_name=_(u'Дом'), max_length=255)

    def __unicode__(self):
        return u'{0}, {1}, {2}'.format(self.city, self.street, self.home)

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Магазин')
        verbose_name_plural = _(u'Магазины')


class Order(models.Model):
    CERTIFICATE_ERROR = _(u'Сертификат уже был использован')
    STATES = Choices(
        ('new', _(u'Ожидает обработки', )),
        ('completed', _(u'Обработан', )),
    )

    number = models.CharField(_(u'Номер заказа'), max_length=255, unique=True, default=uuid.uuid4)
    state = models.CharField(_(u'Статус'), max_length=20, choices=STATES, default=STATES.new)
    date_add = models.DateTimeField(verbose_name=_(u'Дата добавления'), auto_now_add=True, null=True)
    customer = models.ForeignKey(Customer, to_field='number', verbose_name=_(u'Клиент'), null=True, blank=True)
    discount_value = models.FloatField(_(u'Номинал скидки'), null=True, default=0)
    checkout_shop = models.ForeignKey(Shop, to_field='index', verbose_name=_(u'Магазин'), null=True, blank=True,
                                      related_name='orders')
    certificate = models.ForeignKey('checkout.Certificate', to_field='number', null=True, blank=True)
    certificate_value = models.PositiveIntegerField(_(u'Номинал сертификата'), null=True, default=0)
    payment = models.OneToOneField(Payment, null=True, blank=True, related_name='order')

    class Meta:
        verbose_name = _(u'Заказ')
        verbose_name_plural = _(u'Заказы')

    def __unicode__(self):
        return self.number

    @property
    def paid(self):
        return self.payment and self.payment.status == Payment.STATUS.SUCCESS

    def get_full_amount(self):
        result = 0
        for detail in self.order_details.all():
            result += float(detail.price) * detail.amount
        return result
    get_full_amount.allow_tags = True
    get_full_amount.short_description = _(u'Общая стоимость заказа')

    def get_amount_to_pay(self):
        try:
            return self.payment.order_amount
        except AttributeError:
            return None
    get_amount_to_pay.allow_tags = True
    get_amount_to_pay.short_description = _(u'Сумма заказа')

    def get_amount_paid(self):
        try:
            return self.payment.shop_amount
        except AttributeError:
            return None
    get_amount_paid.allow_tags = True
    get_amount_paid.short_description = _(u'Оплаченная сумма')

    def get_performed_datetime(self):
        try:
            return self.payment.performed_datetime
        except AttributeError:
            return None
    get_performed_datetime.allow_tags = True
    get_performed_datetime.short_description = _(u'Дата обработки заказа')

    def get_fio(self):
        try:
            return self.get_customer_address().get_fio()
        except AttributeError:
            return None
    get_fio.allow_tags = True
    get_fio.short_description = _(u'ФИО')

    def get_city(self):
        if self.checkout_shop:
            return self.checkout_shop.city
        address = self.get_other_address() or self.get_customer_address()
        return address.city if address else ''
    get_city.allow_tags = True
    get_city.short_description = _(u'Город')

    def get_count(self):
        return sum([x.amount for x in self.order_details.all()])
    get_count.allow_tags = True
    get_count.short_description = _(u'Количество рубашек в заказе')

    def set_discount(self, amount):
        if self.customer:
            self.discount_value = amount * self.customer.get_discount_value()
            self.save(update_fields=['discount_value'])
        return amount - self.discount_value

    def set_certificate(self, amount):
        if not self.certificate:
            return amount
        if self.certificate.get_value() > amount:
            self.certificate_value = amount
        else:
            self.certificate_value = self.certificate.get_value()
        self.save(update_fields=['certificate_value'])
        return amount - self.certificate_value

    @atomic
    def create_payment(self):
        amount = self.get_full_amount()
        amount = self.set_discount(amount)
        amount = self.set_certificate(amount)
        payment = Payment.objects.create(customer_number=self.number, order_amount=float(amount),
                                         payment_type=Payment.PAYMENT_TYPE.AC)
        self.payment = payment
        self.save(update_fields=['payment'])
        return payment

    def check_certificate(self):
        return self.certificate.get_value() > self.certificate_value

    def save_certificate(self):
        if self.certificate:
            self.certificate.value = self.certificate.get_value() - self.certificate_value
            self.certificate.save(update_fields=['value'])

    def get_customer_address(self):
        return first((lambda x: x.type == CustomerData.ADDRESS_TYPE.customer_address), self.customer_data.all())

    def get_other_address(self):
        return first(lambda x: x.type == CustomerData.ADDRESS_TYPE.other_address, self.customer_data.all())


class CustomerData(models.Model):
    ADDRESS_TYPE = Choices(
        ('customer_address', _(u'Адрес клиента')),
        ('other_address', _(u'Другой адрес (или адрес другого человека)')),
    )
    order = models.ForeignKey(Order, to_field='number', verbose_name=_(u'Заказ'), related_name='customer_data')

    name = models.CharField(_(u'Имя'), max_length=255)
    lastname = models.CharField(_(u'Фамилия'), max_length=255)
    midname = models.CharField(_(u'Отчество'), max_length=255)
    phone = models.CharField(_(u'Телефон'), max_length=255)
    email = models.EmailField(_(u'Телефон'), max_length=255, null=True)

    type = models.CharField(_(u'Тип адреса'), max_length=50, choices=ADDRESS_TYPE,
                            default=ADDRESS_TYPE.customer_address)
    city = models.CharField(_(u'Город'), max_length=255)
    address = models.CharField(_(u'Адрес'), max_length=255)
    index = models.CharField(_(u'Индекс'), max_length=6)

    class Meta:
        verbose_name = _(u'Данные клиента')
        verbose_name_plural = _(u'Данные клиента')
        unique_together = (
            ('order', 'type'),
        )

    def __unicode__(self):
        return u'%s, %s (%s)' % (self.city, self.address, self.get_type_display())

    def get_fio(self):
        return u'%s %s.%s.' % (self.lastname, self.name[0], self.midname[0])


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, verbose_name=_(u'Заказ'), related_name='order_details')
    shirt = models.ForeignKey('backend.Shirt', verbose_name=_(u'Рубашка'))
    amount = models.IntegerField(_(u'Количество'))
    price = models.DecimalField(_(u'Цена'), max_digits=10, decimal_places=2, editable=False, null=True)

    class Meta:
        verbose_name = _(u'Детали заказа')
        verbose_name_plural = _(u'Детали заказа')

    def __unicode__(self):
        return self.order.number

    def get_total(self):
        return self.price * self.amount


class Certificate(models.Model):
    number = models.CharField(_(u'Уникальный номер сертификата'), max_length=50, unique=True, primary_key=True)
    value = models.PositiveIntegerField(_(u'Стоимость'), null=True, default=0)

    def __unicode__(self):
        return u'{0}'.format(self.number)

    class Meta:
        verbose_name = _(u'Сертификат')
        verbose_name_plural = _(u'Сертификаты')

    def get_value(self):
        try:
            return int(self.value)
        except TypeError:
            return 0


class Discount(models.Model):
    customer = models.OneToOneField(Customer, to_field='number', verbose_name=_(u'Уникальный номер пользователя'),
                                    max_length=255, primary_key=True, related_name='discount')
    discount_value = models.FloatField(_(u'Процент скидки'), default=0, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.customer.number)

    class Meta:
        verbose_name = _(u'Скидка')
        verbose_name_plural = _(u'Скидки')


@receiver(payment_completed)
def payment_completed_receiver(sender, *args, **kwargs):
    CostumecodeMailer.send_order_payment_completed(sender.order)
    CostumecodeMailer.send_to_customer_order_payment_completed(sender.order)
