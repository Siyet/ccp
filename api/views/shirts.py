# coding: utf-8

from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from dictionaries import models as dictionaries
from backend import models
from api import serializers

class TemplateShirtsList(ListAPIView):
    serializer_class = serializers.TemplateShirtListSerializer
    queryset = models.Shirt.objects.filter(is_template=True).select_related('fabric')


class TemplateShirtDetails(RetrieveAPIView):
    serializer_class = serializers.TemplateShirtSerializer
    queryset = models.Shirt.objects.filter(is_template=True).select_related('fabric').prefetch_related('shirt_images')