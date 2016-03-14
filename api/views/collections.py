# coding: utf-8
from django.http import Http404

from rest_framework.generics import ListAPIView
from backend.models import Collection
from django.shortcuts import get_object_or_404
from dictionaries.models import ShirtInfo, FabricColor, FabricDesign
from api import serializers


class CollectionsListView(ListAPIView):
    """
    Список коллекций рубашек
    """
    queryset = Collection.objects.all()
    serializer_class = serializers.CollectionSerializer


class ShirtInfoListView(ListAPIView):
    """
    Информация о рубашках для отображения на экране выборе коллекций
    """
    queryset = ShirtInfo.objects.all()
    serializer_class = serializers.ShirtInfoSerializer


class CollectionFabricsList(ListAPIView):
    serializer_class = serializers.FabricSerializer

    def get(self, request, *args, **kwargs):
        """
        Список доступных тканей для выбранной коллекции.
        Может быть отфильтрован по полям "цвет" и "дизайн"
        ---
        parameters:
            - name: color
              type: integer
              paramType: query
              description: цвет (id)
            - name: design
              type: integer
              paramType: query
              description: дизайн (id)
        """
        return super(CollectionFabricsList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        id = self.kwargs['pk']
        collection = get_object_or_404(Collection.objects.select_related('storehouse'), pk=id)

        queryset = collection.fabrics()

        color = self.request.query_params.get('color', None)
        if color is not None:
            queryset = queryset.prefetch_related('colors').filter(colors__id=color)

        design = self.request.query_params.get('design', None)
        if design is not None:
            queryset = queryset.prefetch_related('designs').filter(designs__id=design)

        return queryset


class CollectionFabricColorsList(ListAPIView):
    """
    Список цветов всех тканей, доступных для выбранной коллекции
    """
    serializer_class = serializers.FabricColorSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        collection = get_object_or_404(Collection.objects.select_related('storehouse'), pk=id)
        fabrics = collection.fabrics().values_list('id', flat=True)
        return FabricColor.objects.filter(color_fabrics__id__in=fabrics).distinct()


class CollectionFabricDesignsList(ListAPIView):
    """
    Список дизайнов всех тканей, доступных для выбранной коллекции
    """
    serializer_class = serializers.FabricDesignSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        collection = get_object_or_404(Collection.objects.select_related('storehouse'), pk=id)
        fabrics = collection.fabrics().values_list('id', flat=True)
        return FabricDesign.objects.filter(design_fabrics__id__in=fabrics).distinct()
