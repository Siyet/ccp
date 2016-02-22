# coding: utf-8

from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import pagination
from dictionaries import models as dictionaries
from backend import models
from api import serializers

class TemplateShirtsList(ListAPIView):
    serializer_class = serializers.TemplateShirtListSerializer
    queryset = models.Shirt.objects.filter(is_template=True).select_related('fabric')
    pagination_class = pagination.LimitOffsetPagination

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
    queryset = models.Shirt.objects.filter(is_template=True).select_related('fabric').prefetch_related('shirt_images')