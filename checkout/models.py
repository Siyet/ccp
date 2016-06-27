# coding: utf-8
from django.db import models
from django.utils.text import ugettext_lazy as _

from ordered_model.models import OrderedModel

class Customer(models.Model):
    number = models.CharField(_(u'Уникальный номер пользователя'), max_length=255, unique=True)

    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name = _(u'Клиент')
        verbose_name_plural = _(u'Клиенты')


class Shop(OrderedModel):
    index = models.IntegerField(verbose_name=_(u'Индекс'))
    city = models.CharField(verbose_name=_(u'Город'), max_length=255)
    street = models.CharField(verbose_name=_(u'Улица'), max_length=255)
    home = models.CharField(verbose_name=_(u'Дом'), max_length=255)

    def __unicode__(self):
        return u'{0}, {1}, {2}'.format(self.city, self.street, self.home)

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Магазин')
        verbose_name_plural = _(u'Магазины')


class Order(models.Model):
    number = models.CharField(_(u'Номер заказа'), max_length=255, unique=True)
    customer = models.ForeignKey(Customer, verbose_name=_(u'Клиент'), null=True, blank=True)
    checkout_shop = models.ForeignKey(Shop, verbose_name=_(u'Магазин'), null=True, blank=True, related_name='orders')

    name = models.CharField(_(u'Имя'), max_length=255)
    lastname = models.CharField(_(u'Фамилия'), max_length=255)
    midname = models.CharField(_(u'Отчество'), max_length=255)

    phone = models.CharField(_(u'Телефон'), max_length=255)
    city = models.CharField(_(u'Город'), max_length=255)
    address = models.CharField(_(u'Адрес'), max_length=255)
    index = models.CharField(_(u'Индекс'), max_length=6)
    email = models.EmailField(_(u'E-mail'))

    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name = _(u'Заказ')
        verbose_name_plural = _(u'Заказы')


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, verbose_name=_(u'Заказ'))
    shirt = models.ForeignKey('backend.Shirt', verbose_name=_(u'Рубашка'))
    amount = models.IntegerField(_(u'Количество'))

    def __unicode__(self):
        return self.order.number

    class Meta:
        verbose_name = _(u'Детали заказа')
        verbose_name_plural = _(u'Детали заказа')


class Payment(models.Model):
    order = models.OneToOneField(Order, verbose_name=_(u'Заказ'))
    paid = models.BooleanField(_(u'Оплачено'))


class Certificate(models.Model):
    number = models.CharField(_(u'Уникальный номер сертификата'), max_length=50, unique=True, primary_key=True)
    value = models.PositiveIntegerField(_(u'Стоимость'), null=True, default=0)

    def __unicode__(self):
        return u'{0}'.format(self.number)

    class Meta:
        verbose_name = _(u'Сертификат')
        verbose_name_plural = _(u'Сертификаты')


class Discount(models.Model):
    customer = models.OneToOneField(Customer, to_field='number', verbose_name=_(u'Уникальный номер пользователя'),
                                    max_length=255, primary_key=True)
    discount_value = models.FloatField(_(u'Процент скидки'), default=0, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.customer.number)

    class Meta:
        verbose_name = _(u'Скидка')
        verbose_name_plural = _(u'Скидки')
