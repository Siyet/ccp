# coding: utf-8
import django_filters
from drf_multiple_model.views import MultipleModelAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import pagination
from rest_framework import filters
from backend import models
from dictionaries import models as dictionaries
from api import serializers


class TemplateShirtsFilter(filters.FilterSet):
    fabric = django_filters.ModelMultipleChoiceFilter(queryset=models.Fabric.objects.all())

    class Meta:
        model = models.Shirt
        fields = ['fabric', 'fabric__colors', 'fabric__designs']


class TemplateShirtsList(ListAPIView):
    serializer_class = serializers.TemplateShirtListSerializer
    queryset = models.Shirt.objects.filter(is_template=True).select_related('fabric', 'collection__storehouse').\
        prefetch_related('collection__storehouse__prices')
    pagination_class = pagination.LimitOffsetPagination
    filter_class = TemplateShirtsFilter

    def get(self, request, *args, **kwargs):
        """
        Список рубашек для отображения в разделе "витрина.
        ---
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
        return super(TemplateShirtsList, self).get(request, *args, **kwargs)


class TemplateShirtDetails(RetrieveAPIView):
    serializer_class = serializers.TemplateShirtSerializer
    queryset = models.Shirt.objects.filter(is_template=True).select_related('fabric', 'collection__storehouse').\
        prefetch_related('shirt_images', 'collection__storehouse__prices')


class TemplateShirtFilter(MultipleModelAPIView):

    def get_queryList(self):
        queryList = (
            (models.Fabric.objects.filter(shirt__isnull=False).distinct(), serializers.FabricSerializer),
            (dictionaries.FabricColor.objects.filter(color_fabrics__shirt__isnull=False).distinct(), serializers.FabricColorSerializer),
            (dictionaries.FabricDesign.objects.filter(design_fabrics__shirt__isnull=False).distinct(), serializers.FabricDesignSerializer),
        )
        return queryList
