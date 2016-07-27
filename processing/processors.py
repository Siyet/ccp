import os

from django.conf import settings
import numpy as np
from PIL import Image

from processing.rendering.compose import Composer


def localpath(file):
    return os.path.join(settings.STATIC_ROOT, file)


class ComposeSample(object):
    def __init__(self, cached_file, tiling, shadow):
        self.tiling = tiling
        self.shadow = shadow
        self.cached_file = cached_file

    def process(self, img):

        texture = self.cached_file
        uv = np.load(localpath("sample/UV.npy"))
        light = Image.open(localpath("sample/LIGHT.png"))
        shadow = Image.open(localpath("sample/AO.png")) if self.shadow else None
        return Composer.create(texture, uv, light, shadow, AA=False)
