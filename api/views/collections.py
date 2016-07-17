# coding: utf-8
from django.http import Http404

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.models import Collection, AccessoriesPrice, ContrastDetails, Dickey
from django.shortcuts import get_object_or_404
from django.utils.text import ugettext_lazy as _
from dictionaries import models as dictionaries
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
    queryset = dictionaries.ShirtInfo.objects.all()
    serializer_class = serializers.ShirtInfoSerializer


class CollectionFabricsList(APIView):

    def get(self, request, *args, **kwargs):
        """
        Список доступных тканей для выбранной коллекции.
        Может быть отфильтрован по полям "цвет" и "дизайн"
        ---
        parameters:
            - name: color
              type: integer
              paramType: query
              description: цвет (id)
            - name: design
              type: integer
              paramType: query
              description: дизайн (id)
            - name: thickness
              type: string
              paramType: query
              description: толщина ткани
            - name: fabric_type
              type: string
              paramType: query
              description: тип ткани
        """
        collection = get_object_or_404(Collection.objects.select_related('storehouse'), pk=kwargs.get('pk'))
        collection.prices = collection.storehouse.prices.values('fabric_category', 'price')
        queryset = collection.fabrics().select_related('texture')
        color = self.request.query_params.get('color', None)
        if color is not None:
            queryset = queryset.prefetch_related('colors').filter(colors__id=color)

        design = self.request.query_params.get('design', None)
        if design is not None:
            queryset = queryset.prefetch_related('designs').filter(designs__id=design)

        thickness = self.request.query_params.get('thickness', None)
        if thickness is not None:
            queryset = queryset.filter(thickness__title=thickness)

        fabric_type = self.request.query_params.get('fabric_type', None)
        if fabric_type is not None:
            queryset = queryset.filter(fabric_type__title=fabric_type)

        for fabric in queryset:
            fabric.cached_collection = collection

        return Response(serializers.FabricSerializer(queryset, many=True, context={'request': request}).data)


class CollectionFabricColorsList(ListAPIView):
    """
    Список цветов всех тканей, доступных для выбранной коллекции
    """
    serializer_class = serializers.FabricColorSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        collection = get_object_or_404(Collection.objects.select_related('storehouse'), pk=id)
        fabrics = collection.fabrics().values_list('id', flat=True)
        return dictionaries.FabricColor.objects.filter(color_fabrics__id__in=fabrics).distinct()


class CollectionFabricDesignsList(ListAPIView):
    """
    Список дизайнов всех тканей, доступных для выбранной коллекции
    """
    serializer_class = serializers.FabricDesignSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        collection = get_object_or_404(Collection.objects.select_related('storehouse'), pk=id)
        fabrics = collection.fabrics().values_list('id', flat=True)
        return dictionaries.FabricDesign.objects.filter(design_fabrics__id__in=fabrics).distinct()


class CollectionHardnessList(ListAPIView):
    """
    Список доступных для коллекции вариантов жесткости
    """
    serializer_class = serializers.HardnessSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        collection = get_object_or_404(Collection.objects.prefetch_related('hardness'), pk=id)
        return collection.hardness.all()


class CollectionStaysList(ListAPIView):
    """
    Список доступных для коллекции вариантов косточек воротника
    """
    serializer_class = serializers.StaysSerializer

    def get_queryset(self):
        collection = get_object_or_404(Collection.objects.prefetch_related('stays'), pk=self.kwargs['pk'])
        return collection.stays.all()


class CollectionAccessoriesPriceList(APIView):
    model = None

    def get(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.prefetch_related('stays'), pk=self.kwargs['pk'])
        prices = AccessoriesPrice.objects.filter(collections=collection, content_type__app_label='backend', content_type__model=self.model.__name__.lower()).distinct().first()
        result = [{'key': False, 'value': _(u'Не использовать'), 'extra_price': None}]
        if prices:
            result.append({'key': True, 'value': _(u'Использовать'), 'extra_price': prices.price})
        return Response(result)


class CollectionContrastDetailsList(CollectionAccessoriesPriceList):
    """
    Доступные варианты для контрастных тканей
    """
    model = ContrastDetails


class CollectionDickeyList(CollectionAccessoriesPriceList):
    """
    Доступные варианты для манишки
    """
    model = Dickey


class CollectionStitchesList(APIView):
    """
    Список доступных для коллекции вариантов отстрочек и цветов
    """

    def get(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.prefetch_related('stitches'), pk=self.kwargs['pk'])
        return Response({
            'elements': [{'id': x.pk, 'title': x.title} for x in collection.stitches.all()],
            'colors': [{'id': x.pk, 'title': x.title, 'color': x.color} for x in dictionaries.StitchColor.objects.all()],
        })
