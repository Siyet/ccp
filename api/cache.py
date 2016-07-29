# coding: utf-8

import os
from hashlib import sha1
import json

from django.conf import settings
from django.core.cache import cache

from backend.models import Fabric, FabricPrice
from processing.models import Texture
from processing.rendering.builder import ShirtBuilder


class ShirtImageCache(object):
    @staticmethod
    def get_image_url(data, projection):
        data['projection'] = projection
        key = sha1(json.dumps(data, sort_keys=True)).hexdigest()
        filename = "%s.png" % key

        full_path = os.path.join(settings.RENDER_CACHE_PATH, filename)
        if not os.path.isfile(full_path):
            builder = ShirtBuilder(data, projection)
            image = builder.build_shirt()
            image.save(full_path)
            # TODO: придумать механизм кеширования получше
            cache.set(filename, TempFileToken(full_path), timeout=5 * 60)

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
