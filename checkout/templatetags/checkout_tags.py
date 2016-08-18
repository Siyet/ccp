from django.template import Library
from processing.rendering.image_cache import ShirtImageCache
from processing.models import PROJECTION, CACHE_RESOLUTION

register = Library()

_static = None


@register.simple_tag
def shirt_image(shirt):
    (path, name) = ShirtImageCache.get_image_path_for_model(shirt, PROJECTION.front, CACHE_RESOLUTION.preview)
    return path