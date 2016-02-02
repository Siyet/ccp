# coding: utf-8

from rest_framework.generics import ListAPIView
from backend.models import Collection
from dictionaries.models import ShirtInfo
from api import serializers

class CollectionsListView(ListAPIView):
    """
    Список коллекций рубашек
    """
    queryset = Collection.objects.all()
    serializer_class = serializers.CollectionSerializer


class ShirtInfoListView(ListAPIView):
    """
    Информация о рубашках для отображения на экране выборе коллекций
    """
    queryset = ShirtInfo.objects.all()
    serializer_class = serializers.ShirtInfoSerializer
