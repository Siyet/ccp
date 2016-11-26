# coding: utf-8
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import post_save, pre_save

from backend import models
from dictionaries.models import CustomButtonsType
from pricing import ShirtPriceCalculator


def get_old_shirts(sender, instance, **kwargs):
    if instance.pk is not None and not hasattr(instance, 'ignore_signals'):
        instance.old_shirts = sender.objects.get(pk=instance.pk).get_shirts()


def update_shirts_prices(sender, instance, created, **kwargs):
    if hasattr(instance, 'ignore_signals'):
        return
    # обязательный метод get_shirts для связанных с ценой рубашки моделей
    ids = list(instance.get_shirts())
    ids += getattr(instance, 'old_shirts', [])
    update_prices_by_shirt_ids(ids)


def calculate_shirt_price(sender, instance, **kwargs):
    if isinstance(instance, models.Shirt):
        instance.price = ShirtPriceCalculator().get_price_for_object(instance)


def get_shirts_with_accessories(accessory):
    ct = accessory.content_type
    model = ct.model_class()
    if hasattr(model, "shirt"):
        return list(model.objects.all().values_list('shirt', flat=True).distinct())

    return []


def cache_shirts_with_accessories(sender, instance, **kwargs):
    instance.old_shirts = get_shirts_with_accessories(instance)


def update_price_for_shirts_with_accessories(sender, instance, **kwargs):
    shirt_ids = get_shirts_with_accessories(instance)
    shirt_ids += getattr(instance, 'old_shirts', [])
    update_prices_by_shirt_ids(shirt_ids)


@transaction.atomic
def update_prices_by_shirt_ids(shirt_ids):
    calculator = ShirtPriceCalculator()
    qs = models.Shirt.objects.filter(pk__in=shirt_ids)
    qs = qs.select_related('fabric', 'shawl', 'collection__storehouse', 'custom_buttons__type', 'cuff', 'collar',
                           'dickey')
    qs = qs.prefetch_related('collection__storehouse__prices', 'contrast_details')

    for shirt in qs:
        shirt.price = calculator.get_price_for_object(shirt)
        shirt.save(update_fields=['price'])


# TODO: добавить 2 события для всех связанных моделей с ценой рубашки
pre_save.connect(get_old_shirts, sender=models.FabricPrice)
post_save.connect(update_shirts_prices, sender=models.FabricPrice)

pre_save.connect(cache_shirts_with_accessories, sender=models.AccessoriesPrice)
post_save.connect(update_price_for_shirts_with_accessories, sender=models.AccessoriesPrice)

pre_save.connect(get_old_shirts, sender=models.ShawlOptions)
post_save.connect(update_shirts_prices, sender=models.ShawlOptions)

pre_save.connect(get_old_shirts, sender=CustomButtonsType)
post_save.connect(update_shirts_prices, sender=CustomButtonsType)

pre_save.connect(get_old_shirts, sender=models.ContrastDetails)
post_save.connect(update_shirts_prices, sender=models.ContrastDetails)

pre_save.connect(calculate_shirt_price)
