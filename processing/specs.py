from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit
from imagekit.utils import get_field_info
from .processors import ComposeSample
from django.conf import settings

class Generators(object):
    sample = 'costumecode:sample'
    sample_thumbnail = 'costumecode:sample_thumbnail'

class TextureSampleThumbnail(ImageSpec):
    format = 'JPEG'
    options = {'quality': 80}
    processors =  [ResizeToFit(*settings.FABRIC_SAMPLE_THUMBNAIL_SIZE)]


class TextureSample(ImageSpec):
    format = 'JPEG'
    options = {'quality': 80}

    @property
    def processors(self):
        instance, field_name = get_field_info(self.source)
        return [
            ComposeSample(texture=instance),
            ResizeToFit(*settings.FABRIC_SAMPLE_SIZE)
        ]


register.generator(Generators.sample, TextureSample)
register.generator(Generators.sample_thumbnail, TextureSampleThumbnail)
