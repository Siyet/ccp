# coding: utf-8

from rest_framework.generics import ListAPIView
from api import serializers
from dictionaries.models import FAQ


__all__ = ['FAQListView']


class FAQListView(ListAPIView):
    """
    Список вопросов и ответов
    """
    queryset = FAQ.objects.all()
    serializer_class = serializers.FAQSerializer
