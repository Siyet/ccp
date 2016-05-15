# coding: utf-8

from rest_framework.generics import ListAPIView
from api import serializers
from backend import models


class StoreListView(ListAPIView):
    """
    Список магазинов для самовывоза
    """
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer
