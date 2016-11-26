# coding: utf-8

from django.contrib.contenttypes.models import ContentType

from backend import models as backend
from core.utils import first


def _cached_price(key_func):
    def dec(fn):
        def wrapped(obj, *args, **kwargs):
            key = key_func(*args, **kwargs)
            if not key:
                return 0
            if not key in obj.cached_prices:
                obj.cached_prices[key] = fn(obj, *args, **kwargs)
            return obj.cached_prices[key]

        return wrapped

    return dec


class ShirtPriceCalculator(object):
    cached_prices = {}

    def get_price_for_object(self, shirt):
        price = 0

        # Платок
        price += self._extra_price_for_part(shirt.shawl)

        # Кастомные пуговицы
        buttons = shirt.custom_buttons
        if buttons:
            price += buttons.type.extra_price

        # Манишка
        price += self._extra_price_for_model(getattr(shirt, 'dickey', None))

        # Контрастные детали
        if shirt.contrast_details.count() > 0:
            price += self._extra_price_for_model(backend.ContrastDetails)

        # Ткань
        price += self._fabric_price(shirt.fabric, shirt.collection)

        return price

    def get_price_for_dictionary(self, shirt_data):
        price = 0

        price += self._price_for_part_by_id(backend.ShawlOptions, shirt_data.pop("shawl", None))

        buttons_id = shirt_data.pop("custom_buttons", None)
        if buttons_id:
            buttons = backend.CustomButtons.objects.filter(pk=buttons_id).first()
            if buttons:
                price += buttons.type.extra_price

        if shirt_data.pop('dickey') is not None:
            price += self._extra_price_for_model(backend.Dickey)

        collection = backend.Collection.objects.get(pk=shirt_data.pop('collection'))
        contrast_details = shirt_data.pop('contrast_details')
        # контрастные детали в эксклюзивной коллекции
        exclusive_details = collection.contrast_details and contrast_details
        # "воротник и манжеты полностью белые" в бизнес коллекции
        business_details = contrast_details is not None and not collection.contrast_details
        if business_details or exclusive_details:
            price += self._extra_price_for_model(backend.ContrastDetails)

        fabric = backend.Fabric.objects.get(pk=shirt_data.pop('fabric'))
        price += self._fabric_price(fabric, collection)
        return price

    @_cached_price(key_func=lambda model, id: (model.__name__, id))
    def _price_for_part_by_id(self, model, id):
        if not id:
            return 0

        part = model.objects.get(pk=id)
        return self._extra_price_for_part(part)

    def _extra_price_for_part(self, part):
        if part is None:
            return 0
        return part.extra_price

    @_cached_price(key_func=lambda m: m._meta.model_name if m else None)
    def _extra_price_for_model(self, model):
        if model is None:
            return 0
        ct = ContentType.objects.get_for_model(model)
        model_price = backend.AccessoriesPrice.objects.filter(content_type=ct).first()
        if model_price:
            return model_price.price
        return 0

    @_cached_price(key_func=lambda f, c: (f.id, c.id))
    def _fabric_price(self, fabric, collection):
        fabric_price_filter = lambda x: x.fabric_category_id == fabric.category_id
        fabric_price = first(fabric_price_filter, collection.storehouse.prices.all())
        if fabric_price is not None:
            return fabric_price.price

        return 0
