from hashlib import sha1
import json
import os

from django.conf import settings

from PIL import Image

from processing.models import CACHE_RESOLUTION
from processing.rendering.builders.factory import ShirtBuilderFactory
from api.serializers import ShirtDetailsSerializer


class ShirtImageCache(object):
    compose_parts = ['collar', 'collection', 'cuff', 'pocket', 'custom_buttons_type', 'custom_buttons',
                     'sleeve', 'hem', 'placket', 'tuck', 'back', 'dickey', 'fabric', 'yoke', 'contrast_details',
                     'contrast_stitches', 'initials']

    @staticmethod
    def get_image_url_for_model(shirt, projection, resolution):
        data = ShirtDetailsSerializer(instance=shirt).data
        return ShirtImageCache.get_image_url(data, projection, resolution)

    @staticmethod
    def get_image_path_for_model(shirt, projection, resolution):
        data = ShirtDetailsSerializer(instance=shirt).data
        return ShirtImageCache.get_image_path(data, projection, resolution)

    @staticmethod
    def get_image_path(data, projection, resolution):
        def path_for_key(key):
            filename = "%s_%s_%s.png" % (key, projection, resolution)
            return os.path.join(settings.RENDER_CACHE_PATH, filename), filename

        resolution = resolution or CACHE_RESOLUTION.preview
        # filter out irrelevant keys
        data_keys = data.keys()
        data = { key: data[key] for key in ShirtImageCache.compose_parts if key in data_keys }

        base_key = sha1(json.dumps(data)).hexdigest()

        initials = data.pop('initials')
        key = sha1(json.dumps(data)).hexdigest()
        (full_path, filename) = path_for_key(key)
        image = None
        builder = ShirtBuilderFactory.get_builder_for_shirt(data, projection, resolution)
        if not os.path.isfile(full_path):
            image = builder.build_shirt()
            image.save(full_path)
        # only append initials
        if initials:
            image = image or Image.open(full_path)
            builder.add_initials(image, initials, projection, data['pocket'])
            (full_path, filename) = path_for_key(base_key)
            image.save(full_path)

        return (full_path, filename)

    @staticmethod
    def get_image_url(data, projection, resolution):
        # TODO: revert cache resolution
        resolution = CACHE_RESOLUTION.preview

        (full_path, filename) = ShirtImageCache.get_image_path(data, projection, resolution)
        return os.path.join(settings.RENDER_CACHE_URL, filename)
