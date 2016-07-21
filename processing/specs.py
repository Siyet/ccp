from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit
from imagekit.utils import get_field_info
from .processors import ComposeSample
from django.conf import settings
from os import path

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
        if not bool(instance.cache):
            return []
        if not path.isfile(instance.cache.path):
            return []

        return [
            ComposeSample(instance.cache.path, instance.tiling, instance.needs_shadow),
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
