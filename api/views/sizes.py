# coding: utf-8

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.views.mixins import FilterHelpersMixin
from dictionaries.models import Size, SizeOptions, SleeveLength
from api import serializers


class SizeOptionsList(ListAPIView):
    """
    Список опций для выбора размера на экране "Размеры"
    """
    queryset = SizeOptions.objects.all()
    serializer_class = serializers.SizeOptionSerializer


class SizesList(FilterHelpersMixin, APIView):
    """
    Список конкретных размеров рубашек для отображения в выпадающем списке на экране "Размеры"
    """

    def get(self, request, *args, **kwargs):
        sleeve_options = SleeveLength.objects.values('id', 'title')
        return Response([
            self.build_filter(u'Размер', 'size', list(Size.objects.values('size', 'order'))),
            self.build_filter(u'Длина рукава', 'sleeve_length', sleeve_options)
        ])
