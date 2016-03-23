# coding: utf-8

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
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


class CustomButtonsTypeList(ListAPIView):
    """
    Список типов пуговиц
    """
    serializer_class = serializers.CustomButtonsTypeSerializer
    queryset = dictionaries.CustomButtonsType.objects.prefetch_related('buttons')


class ShawlOptionsList(ListAPIView):
    """
    Список настроек платка
    """
    serializer_class = serializers.ShawlOptionsSerializer
    queryset = models.ShawlOptions.objects.all()


class TuckOptionsList(APIView):
    """
    Список вариантов вытачек
    """

    def get(self, request, *args, **kwargs):
        return Response([{'key': x[0], 'value': unicode(x[1])} for x in models.Shirt.TUCK_OPTIONS])


class ClaspOptionsList(APIView):
    """
    Список вариантов застежек
    """

    def get(self, request, *args, **kwargs):
        return Response([{'key': x[0], 'value': unicode(x[1])} for x in models.Shirt.CLASP_OPTIONS])


class StitchOptionsList(APIView):
    """
    Список вариантов отстрочек
    """

    def get(self, request, *args, **kwargs):
        return Response([{'key': x[0], 'value': unicode(x[1])} for x in models.Shirt.STITCH])


