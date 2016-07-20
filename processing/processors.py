import os

from django.conf import settings

from .compose import create


def localpath(file):
    return os.path.join(settings.STATIC_ROOT, file)


class ComposeSample(object):
    def __init__(self, cached_file, tiling, shadow):
        self.tiling = tiling
        self.shadow = shadow
        self.cached_file = cached_file

    def process(self, img):
        sample = [
            self.cached_file,
            localpath("sample/UV.npy"),
            localpath("sample/LIGHT.png"),
            localpath("sample/LIGHT.png") if self.shadow else None
        ]
        return create(*sample, AA=False)
