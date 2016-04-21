# coding: utf-8
import django_filters
from django.conf import settings
from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import pagination
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from backend import models
from dictionaries import models as dictionaries
from api import serializers


class TemplateShirtsFilter(filters.FilterSet):
    fabric = django_filters.ModelMultipleChoiceFilter(queryset=models.Fabric.objects.all())
    fabric_type = django_filters.ModelMultipleChoiceFilter(queryset=dictionaries.FabricType.objects.all(), name='fabric__fabric_type')
    collection__sex = django_filters.MultipleChoiceFilter(choices=models.SEX)

    class Meta:
        model = models.Shirt
        fields = ['fabric', 'fabric_type', 'fabric__colors', 'fabric__designs', 'collection__sex']


class TemplateShirtsList(ListAPIView):
    serializer_class = serializers.TemplateShirtListSerializer
    queryset = models.TemplateShirt.objects.available().select_related('fabric__fabric_type').distinct()
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


class TemplateShirtsFiltersList(APIView):

    def build_filter(self, title, name, values):
        return {
            'title': title,
            'id': name,
            'values': values
        }

    def get(self, request, *args, **kwargs):
        """
        Фильтры для списка рубашек
        """
        fabrics = models.Fabric.items.filter(shirt__is_template=True, residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL)
        fabric_types = dictionaries.FabricType.objects.filter(fabrics__shirt__is_template=True, fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL)
        colors = dictionaries.FabricColor.objects.filter(color_fabrics__shirt__is_template=True, color_fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL)
        designs = dictionaries.FabricDesign.objects.filter(design_fabrics__shirt__is_template=True, design_fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL)
        sex = [(x['sex'], models.SEX[x['sex']]) for x in models.Collection.objects.filter(shirts__is_template=True, shirts__fabric__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL).values('sex').distinct()]
        return Response([
            self.build_filter(u'Ткань', u'fabric', list(fabrics.annotate(title=F('code')).values('id', 'title', 'material').distinct())),
            self.build_filter(u'Тип ткани', u'fabric_type', list(fabric_types.values('id', 'title').distinct())),
            self.build_filter(u'Цвет', 'fabric__colors', list(colors.values('id', 'title', 'value').distinct())),
            self.build_filter(u'Дизайн', 'fabric__designs', list(designs.values('id', 'title').distinct())),
            self.build_filter(u'Пол', 'collection__sex', map(lambda pair: {'id': pair[0], 'title': pair[1]}, sex))
        ])
