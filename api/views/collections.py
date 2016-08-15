# coding: utf-8
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django.shortcuts import get_object_or_404
from django.utils.text import ugettext_lazy as _
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin
from last_modified.decorators import last_modified
from lazy import lazy

from backend.models import Collection, AccessoriesPrice, ContrastDetails, Dickey
from dictionaries import models as dictionaries
from api import serializers
from .mixins import CollectionMixin
from api.cache import fabric_last_modified
from api.filters import CollectionFabricsFilter
from django.db.models import Q


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


class CollectionFabricsList(CollectionMixin, ListCacheResponseMixin, ListAPIView):
    """
    Список доступных тканей для выбранной коллекции.
    Может быть отфильтрован по полям "цвет" и "дизайн"
    """
    serializer_class = serializers.FabricSerializer
    filter_class = CollectionFabricsFilter
    filter_backends = (filters.DjangoFilterBackend,)

    @lazy
    def collection(self):
        collection = super(CollectionFabricsList, self).collection
        collection.prices = collection.storehouse.prices.values('fabric_category', 'price')
        return collection

    def get_queryset(self):
        return self.collection.fabrics().select_related('texture').exclude(texture=None).exclude(
            Q(short_description='') & Q(long_description='')
        )

    @last_modified(last_modified_func=fabric_last_modified)
    def get(self, request, *args, **kwargs):
        return super(CollectionFabricsList, self).get(request, *args, **kwargs)

    def get_serializer(self, queryset, **kwargs):
        for fabric in queryset:
            fabric.cached_collection = self.collection
        return super(CollectionFabricsList, self).get_serializer(queryset, **kwargs)


class CollectionFabricColorsList(CollectionMixin, ListAPIView):
    """
    Список цветов всех тканей, доступных для выбранной коллекции
    """
    serializer_class = serializers.FabricColorSerializer

    def get_queryset(self):
        fabrics = self.collection.fabrics().values_list('id', flat=True)
        return dictionaries.FabricColor.objects.filter(color_fabrics__id__in=fabrics).distinct()


class CollectionFabricDesignsList(CollectionMixin, ListAPIView):
    """
    Список дизайнов всех тканей, доступных для выбранной коллекции
    """
    serializer_class = serializers.FabricDesignSerializer

    def get_queryset(self):
        fabrics = self.collection.fabrics().values_list('id', flat=True)
        return dictionaries.FabricDesign.objects.filter(design_fabrics__id__in=fabrics).distinct()


class CollectionHardnessList(CollectionMixin, ListAPIView):
    """
    Список доступных для коллекции вариантов жесткости
    """
    serializer_class = serializers.HardnessSerializer

    def get_queryset(self):
        return self.collection.hardness.all()


class CollectionStaysList(CollectionMixin, ListAPIView):
    """
    Список доступных для коллекции вариантов косточек воротника
    """
    serializer_class = serializers.StaysSerializer

    def get_queryset(self):
        return self.collection.stays.all()


class CollectionAccessoriesPriceList(CollectionMixin, APIView):
    model = None

    def get(self, request, *args, **kwargs):
        prices = AccessoriesPrice.objects.filter(collections=self.collection, content_type__app_label='backend',
                                                 content_type__model=self.model.__name__.lower()).distinct().first()
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


class CollectionThicknessList(CollectionMixin, ListAPIView):
    serializer_class = serializers.ThicknessSerializer

    def get_queryset(self):
        return dictionaries.Thickness.objects.filter(fabrics__in=self.collection.fabrics()).distinct()


class CollectionFabricTypeList(CollectionMixin, ListAPIView):
    serializer_class = serializers.FabricTypeSerializer

    def get_queryset(self):
        return dictionaries.FabricType.objects.filter(fabrics__in=self.collection.fabrics()).distinct()


class CollectionStitchesList(APIView):
    """
    Список доступных для коллекции вариантов отстрочек и цветов
    """

    def get(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.prefetch_related('stitches'), pk=self.kwargs['pk'])
        return Response({
            'elements': [{'id': x.pk, 'title': x.title} for x in collection.stitches.all()],
            'colors': [{'id': x.pk, 'title': x.title, 'color': x.color} for x in
                       dictionaries.StitchColor.objects.all()],
        })
