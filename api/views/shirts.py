# coding: utf-8
import django_filters
from django.conf import settings
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
    queryset = models.TemplateShirt.objects.available().select_related('fabric').distinct()
    pagination_class = pagination.LimitOffsetPagination
    filter_class = TemplateShirtsFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend, )
    ordering_fields = ('price', )

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
    queryset = models.TemplateShirt.objects.available().\
        filter(fabric__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL).\
        select_related('fabric', 'collection__storehouse').prefetch_related('shirt_images').distinct()


def build_filter(title, name, values):
    return {
        'filter__title': title,
        'filter__name': name,
        'values': values
    }


class TemplateShirtsFiltersList(APIView):

    def get(self, request, *args, **kwargs):
        return Response([
            build_filter(u'Ткань', u'fabric', list(models.Fabric.objects.filter(shirt__is_template=True, residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL).values_list('id', 'code').distinct())),
            build_filter(u'Цвет', 'fabric__colors', list(dictionaries.FabricColor.objects.filter(color_fabrics__shirt__is_template=True, color_fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL).values_list('id', 'title').distinct())),
            build_filter(u'Дизайн', 'fabric__designs', list(dictionaries.FabricDesign.objects.filter(design_fabrics__shirt__is_template=True, design_fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL).values_list('id', 'title').distinct())),
            build_filter(u'Пол', 'collection__sex', [(x['sex'], models.SEX[x['sex']]) for x in models.Collection.objects.filter(shirts__is_template=True, shirts__fabric__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL).values('sex').distinct()]),
        ])
