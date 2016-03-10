# coding: utf-8
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from backend.models import FabricPrice, Shirt


def get_old_shirts(sender, instance, **kwargs):
        if instance.pk is not None:
            instance.old_shirts = sender.objects.get(pk=instance.pk).get_shirts()


def calculate_shirts_price(sender, instance, created, **kwargs):
    with transaction.atomic():
        # обязательный метод get_shirts для связанных с ценой рубашки моделей
        query = Q(pk__in=instance.get_shirts())
        if not created:
            query |= Q(pk__in=instance.old_shirts)

        for shirt in Shirt.objects.filter(query).select_related('collection__storehouse').\
                prefetch_related('collection__storehouse__prices'):
            shirt.save()

# TODO: добавить 2 события для всех связанных моделей с ценой рубашки
pre_save.connect(get_old_shirts, sender=FabricPrice)
post_save.connect(calculate_shirts_price, sender=FabricPrice)
