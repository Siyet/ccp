# coding: utf-8
from __future__ import absolute_import

from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from checkout import models as checkout


class ShopListView(ListAPIView):
    """
    Список магазинов для самовывоза
    """
    queryset = checkout.Shop.objects.all()
    serializer_class = serializers.ShopSerializer


class CertificateDetailView(APIView):
    """
    Информация о сертификате
    """

    def get(self, request, *args, **kwargs):
        certificate = get_object_or_404(checkout.Certificate, number=kwargs.get('number'))
        serializer = serializers.CertificateSerializer(certificate)
        return Response(serializer.data)
