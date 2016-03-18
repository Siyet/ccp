# coding: utf-8

from rest_framework.generics import ListAPIView
from backend import models
from dictionaries import models as dictionaries
from api import serializers

class CollarTypeList(ListAPIView):
    """
    Список типов воротников
    """
    serializer_class = serializers.CollarTypeSerializer
    queryset = dictionaries.CollarType.objects.all()


class CuffTypeList(ListAPIView):
    """
    Список типов манжет
    """
    serializer_class = serializers.CuffTypeSerializer
    queryset = dictionaries.CuffType.objects.all()


class HemTypeList(ListAPIView):
    """
    Список типов низа рубашки
    """
    serializer_class = serializers.HemTypeSerializer
    queryset = dictionaries.HemType.objects.all()


class BackTypeList(ListAPIView):
    """
    Список типов спинки рубашки
    """
    serializer_class = serializers.BackTypeSerializer
    queryset = dictionaries.BackType.objects.all()


class SleeveTypeList(ListAPIView):
    """
    Список опций воротников
    """
    serializer_class = serializers.SleeveTypeSerializer
    queryset = dictionaries.SleeveType.objects.all()


class PlacketTypeList(ListAPIView):
    """
    Список опций полочки
    """
    serializer_class = serializers.PlacketTypeSerializer
    queryset = dictionaries.PlacketType.objects.all()


class PocketTypeList(ListAPIView):
    """
    Список опций карманов
    """
    serializer_class = serializers.PocketTypeSerializer
    queryset = dictionaries.PocketType.objects.all()


class YokeTypeList(ListAPIView):
    """
    Список опций кокетки
    """
    serializer_class = serializers.YokeTypeSerializer
    queryset = dictionaries.YokeType.objects.all()


class ShawlOptionsList(ListAPIView):
    """
    Список настроек платка
    """
    serializer_class = serializers.ShawlOptionsSerializer
    queryset = models.ShawlOptions.objects.all()
