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
    collection__sex = django_filters.MultipleChoiceFilter(choices=models.SEX)

    class Meta:
        model = models.Shirt
        fields = ['fabric', 'fabric__colors', 'fabric__designs', 'collection__sex']


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


class TemplateShirtsFiltersList(MultipleModelAPIView):

    def get_queryList(self):
        queryList = (
            (models.Fabric.objects.filter(shirt__is_template=True).distinct(), serializers.FabricSerializer, 'fabric'),
            (dictionaries.FabricColor.objects.filter(color_fabrics__shirt__is_template=True).distinct(), serializers.FabricColorSerializer, 'fabric__colors'),
            (dictionaries.FabricDesign.objects.filter(design_fabrics__shirt__is_template=True).distinct(), serializers.FabricDesignSerializer, 'fabric__designs'),
            (models.Collection.objects.filter(shirts__is_template=True).values('sex').distinct(), serializers.CollectionSexSerializer, 'collection__sex'),
        )
        return queryList
