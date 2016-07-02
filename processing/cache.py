from io import BytesIO
from math import floor, ceil

from django.core.files.base import ContentFile
import numpy as np
from .utils import Submatrix, exr_to_array, rect_to_polygon, image_from_array


class CacheBuilder(object):
    SCALE_MAP = {
        'uv': 2.0,
        'light': 1.0,
        'ao': 1.0,
        'body': 1.0,
    }

    EXR_FIELDS = ('uv', )
    RGB_FIELDS = ('light', 'ao')
    RGBA_FIELDS = ('body',)

    @staticmethod
    def create_cache(instance, fields, cache_model):
        matrices = []

        for field in fields:
            image = getattr(instance, field, None)
            if not image or not image.path:
                continue
            image = getattr(instance, field)
            array = exr_to_array(image.path)
            submatrix = Submatrix(array)
            scale = CacheBuilder.SCALE_MAP.get(field, 1)
            matrices.append((field, submatrix, scale))

        size_array = []
        for _, matrix, scale in matrices:
            size_array.append([floor(x/scale) if i < 2 else ceil(x/scale) for i, x in enumerate(matrix.bbox)])

        (x0, y0, x1, y1) = zip(*size_array)

        bbox = (min(x0), min(y0), max(x1), max(y1))

        for field, matrix, scale in matrices:
            # remove old cache
            instance.cache.filter(source_field=field).delete()
            scaled_bbox = tuple(x*scale for x in bbox)
            bbox_polygon = rect_to_polygon(*scaled_bbox)
            cache = cache_model(source_field=field, source=instance, bounding_box=bbox_polygon)
            matrix.repick(scaled_bbox)
            (buffer, extension) = CacheBuilder.get_buffer(field, matrix)
            filename = "%s_%s_%s.%s" % (instance._meta.model_name, instance.id, field, extension)
            cache.file.save(filename, ContentFile(buffer.getvalue()))

    @staticmethod
    def get_buffer(field, matrix):
        buffer = BytesIO()
        if field in CacheBuilder.EXR_FIELDS:
            extension = 'npy'
            np.save(buffer, matrix.values)
        else:
            extension = 'png'
            channels = ('R', 'G', 'B', 'A') if field in CacheBuilder.RGBA_FIELDS else ('R', 'G', 'B')
            img = image_from_array(matrix.values, channels=channels)
            img.save(buffer, extension)

        return (buffer, extension)



