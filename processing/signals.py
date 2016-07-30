from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Texture
from .cache import CacheBuilder

from os import path


@receiver(post_save, sender=Texture)
def cache_texture(instance, **kwargs):
    if getattr(instance, '_updating_cache', False):
        return
    cache = instance.get_cache()
    has_cache = path.isfile(cache) if cache else False
    if set(instance.changed_fields).intersection(['texture', 'tiling', 'needs_shadow']) or not has_cache:
        instance._updating_cache = True
        CacheBuilder.cache_texture(instance)
        instance._updating_cache = False
        instance.sample.generate(force=True)
        instance.sample_thumbnail.generate(force=True)
