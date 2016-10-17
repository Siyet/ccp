# coding: utf-8

from django.contrib.contenttypes.models import ContentType

from core.utils import first
from backend import models as backend


class ShirtPriceCalculator(object):
    @staticmethod
    def get_price_for_object(shirt):
        price = 0

        # Платок
        price += ShirtPriceCalculator._extra_price_for_part(shirt.shawl)

        # Кастомные пуговицы
        buttons = shirt.custom_buttons
        if buttons:
            price += buttons.type.extra_price

        # Манишка
        price += ShirtPriceCalculator._extra_price_for_model(getattr(shirt, 'dickey', None))

        # Контрастные детали
        if shirt.contrast_details.count() > 0:
            price += ShirtPriceCalculator._extra_price_for_model(backend.ContrastDetails)

        # Ткань
        price += ShirtPriceCalculator._fabric_price(shirt.fabric, shirt.collection)

        return price

    @staticmethod
    def get_price_for_dictionary(shirt_data):
        price = 0

        price += ShirtPriceCalculator._price_for_part_by_id(backend.ShawlOptions, shirt_data.pop("shawl", None))

        buttons_id = shirt_data.pop("custom_buttons", None)
        if buttons_id:
            buttons = backend.CustomButtons.objects.filter(pk=buttons_id).first()
            if buttons:
                price += buttons.type.extra_price

        if shirt_data.pop('dickey') is not None:
            price += ShirtPriceCalculator._extra_price_for_model(backend.Dickey)

        collection = backend.Collection.objects.get(pk=shirt_data.pop('collection'))
        contrast_details = shirt_data.pop('contrast_details')
        # контрастные детали в эксклюзивной коллекции
        exclusive_details = collection.contrast_details and contrast_details
        # "воротник и манжеты полностью белые" в бизнес коллекции
        business_details = contrast_details is not None and not collection.contrast_details
        if business_details or exclusive_details:
            price += ShirtPriceCalculator._extra_price_for_model(backend.ContrastDetails)

        fabric = backend.Fabric.objects.get(pk=shirt_data.pop('fabric'))
        price += ShirtPriceCalculator._fabric_price(fabric, collection)
        return price

    @staticmethod
    def _price_for_part_by_id(model, id):
        if not id:
            return 0

        part = model.objects.get(pk=id)
        return ShirtPriceCalculator._extra_price_for_part(part)

    @staticmethod
    def _extra_price_for_part(part):
        if part is None:
            return 0
        return part.extra_price

    @staticmethod
    def _extra_price_for_model(model):
        if model is None:
            return 0

        ct = ContentType.objects.get_for_model(model)
        model_price = backend.AccessoriesPrice.objects.filter(content_type=ct).first()
        if model_price:
            return model_price.price
        return 0

    @staticmethod
    def _fabric_price(fabric, collection):
        fabric_price_filter = lambda x: x.fabric_category_id == fabric.category_id
        fabric_price = first(fabric_price_filter, collection.storehouse.prices.all())
        if fabric_price is not None:
            return fabric_price.price

        return 0
