from django.template import Library
from processing.rendering.image_cache import ShirtImageCache
from processing.models import PROJECTION, CACHE_RESOLUTION

import os

from django.conf import settings

register = Library()

_static = None


@register.simple_tag
def shirt_image(shirt):
    (path, name) = ShirtImageCache.get_image_path_for_model(shirt, PROJECTION.front, CACHE_RESOLUTION.preview)
    return path

@register.simple_tag
def abs(rel):
    return os.path.join(settings.BASE_DIR, rel)

@register.simple_tag
def abs_static(rel):
    return os.path.join(settings.STATIC_ROOT, rel)
