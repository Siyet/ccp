from io import BytesIO
from math import floor, ceil
from copy import copy

from django.core.files.base import ContentFile
import numpy as np

from PIL import Image

from processing.models import BodyConfiguration
from .utils import Matrix, Submatrix, exr_to_array, image_from_array

RENDER_SIZE = (4096, 4096)


class CacheBuilder(object):
    SCALE_MAP = {
        'uv': 2.0,
        'light': 1.0,
        'ao': 1.0,
        'body': 1.0,
    }

    EXR_FIELDS = ('uv',)
    RGBA_FIELDS = ('image', 'light', 'ao')
    L_FIELDS = ('uv_alpha',)

    @staticmethod
    def create_cache(instance, fields, cache_model):
        matrices = []

        for field in fields:
            image = getattr(instance, field, None)
            if not image or not image.path:
                continue
            image = getattr(instance, field)
            array = exr_to_array(image.path)
            if field == 'uv':
                size = array.shape[:2]
                array[..., 0] *= size[0]
                array[..., 1] *= size[1]

            if isinstance(instance.content_object, BodyConfiguration):
                matrix = Matrix(array)
            else:
                matrix = Submatrix(array)
            scale = CacheBuilder.SCALE_MAP.get(field, 1)
            matrices.append((field, matrix, scale))

        size_array = []
        for _, matrix, scale in matrices:
            size_array.append([floor(x / scale) if i < 2 else ceil(x / scale) for i, x in enumerate(matrix.bbox)])

        (x0, y0, x1, y1) = zip(*size_array)

        bbox = (min(x0), min(y0), max(x1), max(y1))

        if 'uv' in fields:
            (_, matrix, scale) = next(mx for mx in matrices if mx[0] == 'uv')
            alpha = copy(matrix)
            alpha._source = matrix._source[..., 3]
            matrix._source = matrix._source[..., :2] # cut redundant channels from matrix
            matrices.append(('uv_alpha', alpha, scale))

        for field, matrix, scale in matrices:
            # remove old cache
            instance.cache.filter(source_field=field).delete()
            scaled_bbox = tuple(x * scale for x in bbox)
            matrix.repick(scaled_bbox)

            (buffer, extension) = CacheBuilder.get_buffer(field, matrix.values)
            filename = "%s_%s_%s.%s" % (instance._meta.model_name, instance.id, field, extension)
            position = tuple(int(x) for x in scaled_bbox[:2])[::-1]
            if field == 'uv_alpha':
                position = tuple(x/2 for x in position)
            cache = cache_model(source_field=field, source=instance, position=position)
            cache.file.save(filename, ContentFile(buffer.getvalue()))

    @staticmethod
    def get_buffer(field, array):
        buffer = BytesIO()
        if field in CacheBuilder.EXR_FIELDS:
            extension = 'npy'
            np.save(buffer, array)
        elif field in CacheBuilder.L_FIELDS:
            extension = 'png'
            array = (array * 255.0).astype('uint8')
            img = Image.fromarray(array, mode='L')
            img = img.resize((x / 2 for x in img.size), Image.LANCZOS)
            img.save(buffer, extension)
        else:
            extension = 'png'
            channels = ('R', 'G', 'B', 'A') if field in CacheBuilder.RGBA_FIELDS else ('R', 'G', 'B')
            img = image_from_array(array, channels=channels)
            img.save(buffer, extension)

        return (buffer, extension)

    @staticmethod
    def cache_texture(texture):
        if not texture.texture:
            return

        img = Image.open(texture.texture.path)
        size = img.size
        tiled_size = tuple(x / texture.tiling for x in RENDER_SIZE)
        if size != tiled_size:
            img = img.resize(tiled_size, Image.LANCZOS)

        texture_arr = np.asarray(img).transpose(1, 0, 2)
        buffer = BytesIO()
        np.save(buffer, texture_arr, allow_pickle=False)
        buffer.flush()
        filename = "%s.npy" % texture.texture.name
        texture.cache.save(filename, ContentFile(buffer.getvalue()))
