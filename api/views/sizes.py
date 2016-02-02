# coding: utf-8

from rest_framework.generics import ListAPIView
from dictionaries.models import Size, SizeOptions
from api import serializers

class SizeOptionsList(ListAPIView):
    """
    Список опций для выбора размера на экране "Размеры"
    """
    queryset = SizeOptions.objects.all()
    serializer_class = serializers.SizeOptionSerializer


class SizesList(ListAPIView):
    """
    Список конкретных размеров рубашек для отображения в выпадающем списке на экране "Размеры"
    """
    queryset = Size.objects.all()
    serializer_class = serializers.SizeSerializer