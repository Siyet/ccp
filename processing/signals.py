from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Texture
from .cache import CacheBuilder


@receiver(pre_save, sender=Texture)
def remember_fields(instance, **kwargs):
    instance._changed_fields = instance.changed_fields


@receiver(post_save, sender=Texture)
def cache_texture(instance, **kwargs):
    if set(instance._changed_fields).intersection(['texture', 'tiling']):
        CacheBuilder.cache_texture(instance)
        instance.sample.generate(force=True)
        instance.sample_thumbnail.generate(force=True)
