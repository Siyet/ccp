# coding: utf-8
from django.conf import settings
from django.utils.text import ugettext_lazy as _
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.views.mixins import FilterHelpersMixin
from backend import models
from dictionaries import models as dictionaries

__all__ = [
    'CollarTypeList', 'CuffTypeList', 'HemTypeList', 'BackTypeList', 'PocketTypeList',
    'PlacketTypeList', 'SleeveTypeList', 'YokeTypeList', 'CustomButtonsTypeList', 'ShawlOptionsList',
    'ClaspOptionsList', 'StitchOptionsList', 'TemplateInitialsList', 'DickeyList', 'PricesList'
]


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


class TemplateInitialsList(APIView):
    def build_filter(self, title, name, values):
        return {
            'title': title,
            'id': name,
            'values': values
        }

    def get(self, request, *args, **kwargs):
        """
        Список параметров для инициалов
        """
        colors = dictionaries.Color.objects.values('id', 'title', 'color')
        fonts = dictionaries.Font.objects.values('id', 'title', 'font')
        return Response([
            self.build_filter(_(u'Цвет'), 'color', list(colors)),
            self.build_filter(_(u'Шрифт'), 'font', map(
                lambda x: {'id': x['id'], 'title': x['title'], 'font': request.build_absolute_uri(x['font'])}, fonts)),
            self.build_filter(_(u'Позиция'), 'location',
                              [{'key': x[0], 'value': unicode(x[1])} for x in models.Initials.LOCATION]),
        ])


class DickeyList(FilterHelpersMixin, APIView):
    """
    Список тканей и типов манишек
    """

    def get(self, request, *args, **kwargs):
        fabrics = models.Fabric.objects.active.filter(residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL, dickey=True)
        fabrics_data = serializers.BaseFabricSerializer(fabrics.distinct(), many=True,
                                                        context={'request': request}).data
        dickey_types = dictionaries.DickeyType.objects.all()
        dickey_types_data = serializers.DickeyTypeSerializer(dickey_types, many=True, context={'request': request}).data
        return Response([
            self.build_filter(u'Ткань', 'fabric', fabrics_data),
            self.build_filter(u'Тип манишки', 'type', dickey_types_data),
        ])


class PricesList(APIView):
    """Список добавочных стоимостей для компонентов"""

    def get(self, request, *args, **kwargs):
        return Response(data=models.AccessoriesPrice.as_list())
