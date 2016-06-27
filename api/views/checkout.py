# coding: utf-8
from __future__ import absolute_import

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from yandex_kassa.forms import PaymentForm

from api import serializers
from checkout import models as checkout
from checkout.models import Order


class ShopListView(ListAPIView):
    """
    Список магазинов для самовывоза
    """
    queryset = checkout.Shop.objects.all()
    serializer_class = serializers.ShopSerializer


class CertificateDetailView(RetrieveAPIView):
    """
    Информация о сертификате
    """
    queryset = checkout.Certificate.objects.all()
    serializer_class = serializers.CertificateSerializer


class OrderCreateView(CreateAPIView):
    """
    Создание заказа
    """
    queryset = Order.objects.prefetch_related('order_details').all()
    serializer_class = serializers.OrderSerializer


class OrderPaymentData(APIView):
    """
    Получение данных для перехода на страницу оплаты
    """

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(checkout.Order, number=kwargs.get('number'))
        form = PaymentForm()
        data = {field: form.fields[field].initial for field in form.fields}
        data['orderNumber'] = order.number
        data['customerNumber'] = order.number
        data['sum'] = order.payment.order_amount
        data['target'] = form.target
        return Response(data)
