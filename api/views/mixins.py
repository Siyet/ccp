# coding: utf-8

from django.shortcuts import get_object_or_404
from lazy import lazy

from backend.models import Collection


class FilterHelpersMixin(object):
    def build_filter(self, title, name, values):
        """
        Create dict for filter values
        :param title: view title
        :param name: key for model
        :param values: list values
        :return: dict
        """
        return {
            'title': title,
            'id': name,
            'values': values
        }

    def create_key_value_dict(self, key, value):
        """
        Create dict for model list
        :param key: model key
        :param value: model value
        :return: dict
        """
        return {
            'key': key,
            'value': value
        }


class CollectionMixin(object):
    """
    Миксин для получения коллекции из БД или из кэша
    """

    @lazy
    def collection(self):
        collection = get_object_or_404(
            Collection.objects.select_related('storehouse'), pk=self.kwargs.get('pk')
        )
        return collection
