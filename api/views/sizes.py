# coding: utf-8

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.views.mixins import ManyModelsView
from backend.models import Shirt
from dictionaries.models import Size, SizeOptions
from api import serializers


class SizeOptionsList(ListAPIView):
    """
    Список опций для выбора размера на экране "Размеры"
    """
    queryset = SizeOptions.objects.all()
    serializer_class = serializers.SizeOptionSerializer


class SizesList(ManyModelsView, APIView):
    """
    Список конкретных размеров рубашек для отображения в выпадающем списке на экране "Размеры"
    """

    def get(self, request, *args, **kwargs):
        return Response([
            self.build_filter(u'Размер', 'size', list(Size.objects.values('size', 'order'))),
            self.build_filter(u'Талия', 'fit', map(lambda x: self.create_key_value_dict(*x), Shirt.FIT)),
            self.build_filter(u'Длина рукава', 'sleeve_length',
                              map(lambda x: self.create_key_value_dict(*x), Shirt.SLEEVE_LENGTH)),
        ])
