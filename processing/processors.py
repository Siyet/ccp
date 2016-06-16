from .process import create

from django.conf import settings
import os

def localpath(file):
    return os.path.join(settings.STATIC_ROOT, file)

class ComposeSample(object):

    def __init__(self, texture):
        self.texture = texture

    def process(self, img):
        sample = {
            "textures": [self.texture.texture.path],
            "uv":[localpath("sample/UV.exr")],
            "lights": [localpath("sample/LIGHT.exr")],
            "pre_shadows": [localpath("sample/LIGHT.exr")] if self.texture.needs_shadow else [],
            "post_shadows": [],
            "tiling": self.texture.tiling,
            "AA": False
        }
        results = create(**sample)
        return results[0]
