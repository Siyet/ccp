# coding: utf-8

import os
import json
from hashlib import sha1

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import pagination
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.cache import cache

from django.conf import settings

from backend import models
from dictionaries import models as dictionaries
from api import serializers
from api.filters import TemplateShirtsFilter
from api.cache import ShirtImageCache
from processing.rendering.builder import ShirtBuilder


class TemplateShirtsList(ListAPIView):
    serializer_class = serializers.TemplateShirtListSerializer
    queryset = models.TemplateShirt.objects.available().select_related('fabric__fabric_type', 'fabric__thickness')
    pagination_class = pagination.LimitOffsetPagination
    filter_class = TemplateShirtsFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    ordering_fields = ('price',)

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
    queryset = models.TemplateShirt.objects.available(). \
        select_related('fabric', 'collection__storehouse').prefetch_related('shirt_images')


class TemplateShirtsFiltersList(APIView):
    def build_filter(self, title, name, values):
        return {
            'title': title,
            'id': name,
            'values': values
        }

    def build_design_list(self, desings, request):
        return map(
            lambda x: {'id': x.pk, 'title': x.title, 'image': request.build_absolute_uri(x.picture.url)},
            desings
        )

    def get(self, request, *args, **kwargs):
        """
        Фильтры для списка рубашек
        """
        fabric_types = dictionaries.FabricType.objects.filter(
            fabrics__shirt__is_template=True,
            fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL
        )
        thickness = dictionaries.Thickness.objects.filter(
            fabrics__shirt__is_template=True,
            fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL
        )
        colors = dictionaries.FabricColor.objects.filter(
            color_fabrics__shirt__is_template=True,
            color_fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL
        )
        designs = dictionaries.FabricDesign.objects.filter(
            design_fabrics__shirt__is_template=True,
            design_fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL
        )
        collections = models.Collection.objects.filter(
            shirts__is_template=True,
            shirts__fabric__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL
        )

        return Response([
            self.build_filter(u'Коллекция', 'collection', list(collections.values('id', 'title').distinct())),
            self.build_filter(u'Цвет', 'fabric__colors', list(colors.values('id', 'title', 'value').distinct())),
            self.build_filter(u'Тип ткани', u'fabric_type', list(fabric_types.values('id', 'title').distinct())),
            self.build_filter(u'Толщина ткани', u'thickness', list(thickness.values('id', 'title').distinct())),
            self.build_filter(u'Дизайн', 'fabric__designs', self.build_design_list(designs.distinct(), request)),
        ])


class ShirtDetails(RetrieveAPIView):
    """
    Получение информации о рубашке
    """
    serializer_class = serializers.ShirtDetailsSerializer

    queryset = models.Shirt.objects.all()


class ShirtImage(APIView):
    def post(self, request, projection, *args, **kwargs):
        """
        Генерация ссылки на изображение рубашки в заданной проекции.

        ---
        parameters:
          - name: body
            description: json-объект рубашки, см. /api/shirt/{pk}/
            paramType: body
            required: true
          - name: projection
            description: проекция, одно из трех значений (front|side|back)
            paramType: path
            required: true
        """
        data = request.data
        image_url = ShirtImageCache.get_image_url(data, projection)
        print(image_url)
        return Response(request.build_absolute_uri(image_url))
