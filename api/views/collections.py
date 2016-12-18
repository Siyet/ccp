# coding: utf-8
from django.db.models import Q
from django.shortcuts import get_object_or_404
from last_modified.decorators import last_modified
from lazy import lazy
from rest_framework import filters
from rest_framework import pagination
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from api import serializers
from api.cache import fabric_last_modified, ListKeyConstructor
from api.filters import CollectionFabricsFilter
from backend.models import Collection
from dictionaries import models as dictionaries
from .mixins import CollectionMixin

__all__ = [
    'CollectionsListView', 'CollectionFabricDesignsList', 'CollectionFabricsList', 'CollectionFabricColorsList',
    'CollectionHardnessList', 'CollectionStaysList', 'CollectionStitchesList',
    'CollectionThicknessList', 'CollectionFabricTypeList', 'CollectionTuckList',
    'CollectionFitList',
]


class CollectionsListView(ListAPIView):
    """
    Список коллекций рубашек
    """
    queryset = Collection.objects.all()
    serializer_class = serializers.CollectionSerializer


class CollectionFabricsList(CollectionMixin, ListAPIView):
    """
    Список доступных тканей для выбранной коллекции.
    """
    serializer_class = serializers.FabricSerializer
    filter_class = CollectionFabricsFilter
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = pagination.LimitOffsetPagination

    @lazy
    def collection(self):
        collection = super(CollectionFabricsList, self).collection
        collection.prices = collection.storehouse.prices.values('fabric_category', 'price')
        return collection

    def get_queryset(self):
        return self.collection.fabrics().select_related(
            'texture').exclude(texture=None).exclude(
            Q(short_description='') & Q(long_description='')
        ).exclude(dickey=True)

    # TODO: @cache_response(key_func=ListKeyConstructor())

    def list(self, request, *args, **kwargs):
        return super(CollectionFabricsList, self).list(request, *args, **kwargs)

    @last_modified(last_modified_func=fabric_last_modified)
    def get(self, request, *args, **kwargs):
        """
        ---
        parameters_strategy: merge
        parameters:
            - name: limit
              type: integer
              paramType: query
              description: количество записей
            - name: offset
              type: integer
              paramType: query
              description: отступ
        """
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


class CollectionTuckList(CollectionMixin, ListAPIView):
    """
    Список доступных для коллекции вариантов вытачек
    """
    serializer_class = serializers.TuckSerializer

    def get_queryset(self):
        return self.collection.tuck.all()


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


class CollectionFitList(CollectionMixin, ListAPIView):
    serializer_class = serializers.FitSerializer

    def get_queryset(self):
        return self.collection.fits.prefetch_related('sizes')
