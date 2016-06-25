# coding: utf-8
from __future__ import absolute_import

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

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

    """
    queryset = Order.objects.prefetch_related('order_details').all()
    serializer_class = serializers.OrderSerializer
