import os

from django.conf import settings

from .process import create


def localpath(file):
    return os.path.join(settings.STATIC_ROOT, file)


class ComposeSample(object):
    def __init__(self, cached_file, tiling, shadow):
        self.tiling = tiling
        self.shadow = shadow
        self.cached_file = cached_file

    def process(self, img):
        sample = {
            "texture": self.cached_file,
            "uv": [localpath("sample/UV.npy")],
            "lights": [localpath("sample/LIGHT.png")],
            "pre_shadows": [localpath("sample/LIGHT.png")] if self.shadow else [],
            "post_shadows": [],
            "tiling": self.tiling,
            "AA": False
        }
        return create(**sample)
