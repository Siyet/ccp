# coding: utf-8
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import post_save, pre_save

from backend import models
from dictionaries.models import CustomButtonsType
from pricing import ShirtPriceCalculator


def get_old_shirts(sender, instance, **kwargs):
    if instance.pk is not None:
        instance.old_shirts = sender.objects.get(pk=instance.pk).get_shirts()


def calculate_shirts_price(sender, instance, created, **kwargs):
    with transaction.atomic():
        # обязательный метод get_shirts для связанных с ценой рубашки моделей
        query = Q(pk__in=instance.get_shirts())
        if not created:
            query |= Q(pk__in=instance.old_shirts)

        for shirt in models.Shirt.objects.filter(query). \
                select_related('fabric', 'shawl', 'collection__storehouse', 'custom_buttons__type', 'cuff', 'collar',
                               'dickey'). \
                prefetch_related('collection__storehouse__prices', 'contrast_details'):
            shirt.save()


def calculate_shirt_price(sender, instance, **kwargs):
    if isinstance(instance, models.Shirt):
        instance.price = ShirtPriceCalculator.get_price_for_object(instance)


# TODO: добавить 2 события для всех связанных моделей с ценой рубашки
pre_save.connect(get_old_shirts, sender=models.FabricPrice)
post_save.connect(calculate_shirts_price, sender=models.FabricPrice)

pre_save.connect(get_old_shirts, sender=models.AccessoriesPrice)
post_save.connect(calculate_shirts_price, sender=models.AccessoriesPrice)

pre_save.connect(get_old_shirts, sender=models.ShawlOptions)
post_save.connect(calculate_shirts_price, sender=models.ShawlOptions)

pre_save.connect(get_old_shirts, sender=CustomButtonsType)
post_save.connect(calculate_shirts_price, sender=CustomButtonsType)

pre_save.connect(get_old_shirts, sender=models.ContrastDetails)
post_save.connect(calculate_shirts_price, sender=models.ContrastDetails)

pre_save.connect(calculate_shirt_price)
