# coding: utf-8

import os
from hashlib import sha1
import json

from django.conf import settings
from django.core.cache import cache
from PIL import Image

from backend.models import Fabric, FabricPrice
from processing.models import Texture, CACHE_RESOLUTION
from processing.rendering.builder import ShirtBuilder


class ShirtImageCache(object):
    @staticmethod
    def get_image_url(data, projection, resolution):
        def path_for_key(key):
            filename = "%s_%s_%s.png" % (key, projection, resolution)
            return os.path.join(settings.RENDER_CACHE_PATH, filename), filename

        resolution = resolution or CACHE_RESOLUTION.preview
        base_key = sha1(json.dumps(data, sort_keys=True)).hexdigest()
        initials = data.pop('initials')
        key = sha1(json.dumps(data, sort_keys=True)).hexdigest()
        (full_path, filename) = path_for_key(key)
        image = None
        if not os.path.isfile(full_path):
            builder = ShirtBuilder(data, projection, resolution)
            image = builder.build_shirt()
            image.save(full_path)
        # only append initials
        if initials:
            image = image or Image.open(full_path)
            ShirtBuilder.add_initials(image, initials, projection, data['pocket'])
            (full_path, filename) = path_for_key(base_key)
            image.save(full_path)


        return os.path.join(settings.RENDER_CACHE_URL, filename)


class TempFileToken(object):
    def __init__(self, path):
        self.path = path

    def __del__(self):
        if os.path.isfile(self.path):
            os.remove(self.path)


def get_latest_date(model):
    latest = model.objects.values_list('modified').latest('modified')
    return latest[0] if latest else None


def fabric_last_modified(*args, **kwargs):
    dates = map(lambda model: get_latest_date(model), [Fabric, FabricPrice, Texture])
    return max(dates)
