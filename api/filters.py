from rest_framework import filters
import django_filters

from backend import models
from dictionaries import models as dictionaries


class TemplateShirtsFilter(filters.FilterSet):
    fabric = django_filters.ModelMultipleChoiceFilter(queryset=models.Fabric.objects.all())
    fabric_type = django_filters.ModelMultipleChoiceFilter(queryset=dictionaries.FabricType.objects.all(),
                                                           name='fabric__fabric_type')
    thickness = django_filters.ModelMultipleChoiceFilter(queryset=dictionaries.Thickness.objects.all(),
                                                         name='fabric__thickness')
    collection__sex = django_filters.MultipleChoiceFilter(choices=models.SEX)

    class Meta:
        model = models.Shirt
        fields = ['fabric', 'fabric_type', 'thickness', 'fabric__colors', 'fabric__designs', 'collection__sex']


class CollectionFabricsFilter(filters.FilterSet):
    class Meta:
        model = models.Fabric
        fields = ('colors', 'designs', 'fabric_type', 'thickness',)
