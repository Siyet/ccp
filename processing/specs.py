from os import path

from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit
from imagekit.utils import get_field_info
from django.conf import settings

from .models import CACHE_RESOLUTION
from .processors import ComposeSample


class Generators(object):
    sample = 'costumecode:sample'
    sample_thumbnail = 'costumecode:sample_thumbnail'


class TextureSample(ImageSpec):
    format = 'JPEG'
    options = {'quality': 90}
    size = settings.FABRIC_SAMPLE_SIZE

    @property
    def processors(self):
        instance, field_name = get_field_info(self.source)
        cache = instance.cache.filter(resolution=CACHE_RESOLUTION.preview).first()
        if not cache or not path.isfile(cache.file.path):
            return []

        return [
            ComposeSample(cache.file.path, instance.needs_shadow),
            ResizeToFit(*self.size)
        ]


class TextureSampleThumbnail(TextureSample):
    format = 'JPEG'
    options = {'quality': 90}
    processors = [
        ResizeToFit(*settings.FABRIC_SAMPLE_THUMBNAIL_SIZE)
    ]


register.generator(Generators.sample, TextureSample)
register.generator(Generators.sample_thumbnail, TextureSampleThumbnail)
