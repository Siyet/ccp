# coding: utf-8
import django_filters
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import pagination
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
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
    queryset = models.TemplateShirt.objects.filter(fabric__residuals__amount__gt=0).\
        select_related('fabric', 'collection__storehouse').\
        prefetch_related('collection__storehouse__prices').distinct()
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
    queryset = models.TemplateShirt.objects.filter(fabric__residuals__amount__gt=0).\
        select_related('fabric', 'collection__storehouse').\
        prefetch_related('shirt_images', 'collection__storehouse__prices').distinct()


class TemplateShirtsFiltersList(APIView):

    def get(self, request, *args, **kwargs):
        return Response({
            'fabric': list(models.Fabric.objects.filter(shirt__is_template=True, residuals__amount__gt=0).values_list('id', 'code').distinct()),
            'fabric__colors': list(dictionaries.FabricColor.objects.filter(color_fabrics__shirt__is_template=True, color_fabrics__residuals__amount__gt=0).values_list('id', 'title').distinct()),
            'fabric__designs': list(dictionaries.FabricDesign.objects.filter(design_fabrics__shirt__is_template=True, design_fabrics__residuals__amount__gt=0).values_list('id', 'title').distinct()),
            'collection__sex': [(x['sex'], models.SEX[x['sex']]) for x in models.Collection.objects.filter(shirts__is_template=True, shirts__fabric__residuals__amount__gt=0).values('sex').distinct()],
        })
