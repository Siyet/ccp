# coding: utf-8
from __future__ import absolute_import

from rest_framework.generics import ListAPIView, RetrieveAPIView

from api import serializers
from checkout import models as checkout


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
