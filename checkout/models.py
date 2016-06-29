# coding: utf-8
import uuid

from django.db import models
from django.db.transaction import atomic
from django.utils.text import ugettext_lazy as _
from model_utils import Choices

from ordered_model.models import OrderedModel
from yandex_kassa.models import Payment


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

    number = models.CharField(_(u'Номер заказа'), max_length=255, unique=True, default=uuid.uuid4)
    customer = models.ForeignKey(Customer, to_field='number', verbose_name=_(u'Клиент'), null=True, blank=True)
    checkout_shop = models.ForeignKey(Shop, to_field='index', verbose_name=_(u'Магазин'), null=True, blank=True,
                                      related_name='orders')
    certificate = models.ForeignKey('checkout.Certificate', to_field='number', null=True, blank=True)
    payment = models.OneToOneField(Payment, null=True, blank=True, related_name='order')

    class Meta:
        verbose_name = _(u'Заказ')
        verbose_name_plural = _(u'Заказы')

    def __unicode__(self):
        return self.number

    @property
    def paid(self):
        return self.payment and self.payment.status == Payment.STATUS.SUCCESS

    def get_amount(self):
        result = 0
        for detail in self.order_details.all():
            result += float(detail.shirt.price) * detail.amount
        if self.customer:
            result *= 1 - self.customer.get_discount_value()
        if self.certificate:
            cached_result = result
            result -= self.certificate.get_value()
            if result < 0:
                result = 0
            self.certificate.value -= cached_result
            if self.certificate.value < 0:
                self.certificate.value = 0
        return result

    @atomic
    def create_payment(self):
        payment = Payment.objects.create(customer_number=self.number, order_amount=float(self.get_amount()),
                                         payment_type=Payment.PAYMENT_TYPE.AC)
        self.payment = payment
        self.save(update_fields=['payment'])
        return payment

    def check_amount(self):
        return self.get_amount() == self.payment.order_amount

    def save_cert(self):
        self.get_amount()
        if self.certificate:
            self.certificate.save(update_fields=['value'])


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


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, verbose_name=_(u'Заказ'), related_name='order_details')
    shirt = models.ForeignKey('backend.Shirt', verbose_name=_(u'Рубашка'))
    amount = models.IntegerField(_(u'Количество'))

    def __unicode__(self):
        return self.order.number

    class Meta:
        verbose_name = _(u'Детали заказа')
        verbose_name_plural = _(u'Детали заказа')


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
