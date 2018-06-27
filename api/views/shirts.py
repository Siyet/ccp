# coding: utf-8

from django.conf import settings
from django.utils.text import ugettext_lazy as _
from rest_framework import filters
from rest_framework import pagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.filters import TemplateShirtsFilter
from api.views.mixins import FilterHelpersMixin
from backend import models
from backend.pricing import ShirtPriceCalculator
from dictionaries import models as dictionaries
from processing.rendering.image_cache import ShirtImageCache

__all__ = [
    'ShowcaseShirtsListView', 'TemplateShirtDetails', 'TemplateShirtsFiltersList', 'ShirtDetails',
    'ShirtImage', 'ShirtPrice'
]


class ShowcasePagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class ShowcaseShirtsListView(ListAPIView):
    serializer_class = serializers.TemplateShirtListSerializer
    queryset = models.TemplateShirt.objects.available().select_related('fabric__type', 'fabric__thickness')
    pagination_class = ShowcasePagination
    filter_class = TemplateShirtsFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    ordering_fields = ('price',)


    def get(self, request, *args, **kwargs):
        """
        Список рубашек для отображения в разделе "витрина".
        Для фильтрации всех полей возможно использование нескольких значений через запятую:
        ?fabric__type=1,2&fabric__colors=1,2&collection__sex=female,unisex
        ---
        parameters:
            - name: ordering
              type: string
              paramType: query
              description: |
                сортировка по цене, примеры:<br/>
                 /?ordering=price - по возрастанию<br/>
                 /?ordering=-price - по убыванию<br/>
            - name: limit
              type: integer
              paramType: query
              description: количество записей
            - name: offset
              type: integer
              paramType: query
              description: отступ
        """
        return super(ShowcaseShirtsListView, self).get(request, *args, **kwargs)


class TemplateShirtDetails(RetrieveAPIView):
    serializer_class = serializers.TemplateShirtSerializer
    queryset = models.TemplateShirt.objects.available(). \
        select_related('fabric', 'collection__storehouse').prefetch_related('shirt_images')


class TemplateShirtsFiltersList(FilterHelpersMixin, APIView):
    def build_design_list(self, desings, request):
        return map(
            lambda x: {'id': x.pk, 'title': x.title, 'image': request.build_absolute_uri(x.picture.url)},
            desings
        )

    def get_ordering_options(self):
        ordering_fields = ShowcaseShirtsListView.ordering_fields
        ordering_options = []
        for field_key in ordering_fields:
            field = models.Shirt._meta.get_field(field_key)
            ordering_options.append({'id': field_key, 'title': _(u'%s - по возрастанию' % field.verbose_name)})
            ordering_options.append({'id': '-' + field_key, 'title': _(u'%s - по убыванию' % field.verbose_name)})

        return ordering_options

    def get_colors_serializer(self, colors):
        return serializers.FabricColorSerializer(colors, many=True, context={'request': self.request})

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
        colors_serializer = self.get_colors_serializer(colors.distinct())
        designs = dictionaries.FabricDesign.objects.filter(
            design_fabrics__shirt__is_template=True,
            design_fabrics__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL
        )
        collections = models.Collection.objects.filter(
            shirts__is_template=True,
            shirts__fabric__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL
        )

        collections = collections.values('id', 'filter_title').distinct()
        collections_list = [{'id': c['id'], 'title': c['filter_title']} for c in collections]

        return Response([
            self.build_filter(_(u'Коллекция'), 'collection', collections_list),
            self.build_filter(_(u'Цвет'), 'fabric__colors', colors_serializer.data),
            self.build_filter(_(u'Узор'), 'fabric__designs', self.build_design_list(designs.distinct(), request)),
            self.build_filter(_(u'Плетение'), 'fabric__type', list(fabric_types.values('id', 'title').distinct())),
            self.build_filter(_(u'Плотность'), 'fabric__thickness',
                              list(thickness.values('id', 'title').distinct())),
            self.build_filter(_(u'Цена'), 'ordering', self.get_ordering_options())
        ])


class ShirtDetails(RetrieveAPIView):
    """
    Получение информации о рубашке
    """
    serializer_class = serializers.ShirtDetailsSerializer
    queryset = models.Shirt.objects.select_related("fabric")


class ShirtImage(APIView):
    def post(self, request, projection, resolution=None, *args, **kwargs):
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
          - name: resolution
            description: разрешение (preview|full)
            paramType: path
            required: true
        """
        if 'echo' in request.query_params:
            return Response(request.data)
        data = dict(request.data)
        image_url = ShirtImageCache.get_image_url(data, projection, resolution)
        return Response(request.build_absolute_uri(image_url))


class ShirtPrice(APIView):
    def post(self, request, *args, **kwargs):
        """
        Получение цены рубашки.
        ---
        parameters:
          - name: body
            description: json-объект рубашки, см. /api/shirt/{pk}/
            paramType: body
            required: true
        """
        price = ShirtPriceCalculator().get_price_for_dictionary(request.data)
        return Response(price)
