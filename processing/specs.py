from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit
from imagekit.utils import get_field_info
from .processors import ComposeSample
from django.conf import settings

sample_generator_id = 'costumecode:sample'

class TextureSample(ImageSpec):
    format = 'JPEG'
    options = {'quality': 80}

    @property
    def processors(self):
        instance, field_name = get_field_info(self.source)
        return [
            ComposeSample(texture=instance),
            ResizeToFit(width=settings.FABRIC_SAMPLE_SIZE[0], height=settings.FABRIC_SAMPLE_SIZE[1])
        ]


register.generator(sample_generator_id, TextureSample)
