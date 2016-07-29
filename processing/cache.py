from io import BytesIO
from math import floor, ceil
from copy import copy

from django.core.files.base import ContentFile
import numpy as np
from PIL import Image

from core.utils import first
from processing.models import BodyConfiguration, SourceCache
from processing.rendering.utils import Matrix, Submatrix, exr_to_array, image_from_array
from django.contrib.contenttypes.models import ContentType

RENDER_SIZE = (4096, 4096)

EXR_FIELD = 'EXR'
RGBA_FIELD = 'RGBA'
L_FIELD = 'L'
STITCHES = 'S'

class CacheBuilder(object):


    SCALE_MAP = {
        'uv': 2.0,
        'light': 1.0,
        'ao': 1.0,
        'body': 1.0,
    }

    DEFAULT_FIELD_TYPES = {
        'uv': EXR_FIELD,
        'image': RGBA_FIELD,
        'light': RGBA_FIELD,
        'ao': RGBA_FIELD,
        'uv_alpha': L_FIELD,
        'mask': L_FIELD,
        'side_mask': L_FIELD
    }

    @staticmethod
    def create_cache(instance, fields, field_types):
        matrices = []

        for field in fields:
            image = getattr(instance, field, None)
            if not image or not image.path:
                continue
            image = getattr(instance, field)
            try:
                array = exr_to_array(image.path)
            except IOError:
                array = np.asarray(Image.open(image.path)).astype('float32') / 255.0

            if field == 'uv':
                size = array.shape[:2]
                array[..., 0] *= size[0]
                array[..., 1] *= size[1]

            if isinstance(getattr(instance, 'content_object', None), BodyConfiguration):
                matrix = Matrix(array)
            else:
                try:
                    matrix = Submatrix(array)
                except:
                    print(image.path)
                    raise
            scale = CacheBuilder.SCALE_MAP.get(field, 1)
            matrices.append((field, matrix, scale))

        if not matrices:
            raise Exception("Failed to cache source: fields %s are not found; source id: %s" % (fields, instance.id))

        size_array = []
        for _, matrix, scale in matrices:
            size_array.append([floor(x / scale) if i < 2 else ceil(x / scale) for i, x in enumerate(matrix.bbox)])

        (x0, y0, x1, y1) = zip(*size_array)

        bbox = (min(x0), min(y0), max(x1), max(y1))

        if 'uv' in fields:
            (_, matrix, scale) = first(lambda x: x[0] == 'uv', matrices)
            alpha = copy(matrix)
            alpha._source = matrix._source[..., 3]
            matrix._source = matrix._source[..., :2] # cut redundant channels from matrix
            matrix._source = matrix._source.astype('uint16')
            matrices.append(('uv_alpha', alpha, scale))

        for field, matrix, scale in matrices:
            # remove old cache
            instance.cache.filter(source_field=field).delete()
            scaled_bbox = tuple(x * scale for x in bbox)
            matrix.repick(scaled_bbox)
            field_type = field_types.get(field) or CacheBuilder.DEFAULT_FIELD_TYPES.get(field)
            (buffer, extension) = CacheBuilder.get_buffer(field, matrix.values, field_type)
            filename = "%s_%s_%s.%s" % (instance._meta.model_name, instance.id, field, extension)
            position = tuple(int(x) for x in scaled_bbox[:2])[::-1]
            if field_type == L_FIELD:
                position = tuple(x/2 for x in position)
            ct = ContentType.objects.get_for_model(instance)
            cache = SourceCache(source_field=field, object_id=instance.id, content_type=ct, position=position)
            cache.file.save(filename, ContentFile(buffer.getvalue()))

    @staticmethod
    def get_buffer(field, array, field_type):
        buffer = BytesIO()
        if field_type == EXR_FIELD:
            extension = 'npy'
            np.save(buffer, array)
        elif field_type == L_FIELD or field_type == STITCHES:
            extension = 'png'
            array = (array * 255.0).astype('uint8')
            if len(array.shape) > 2:
                if array.shape[2] > 1:
                    array = array[..., -1] # only take alpha
                array = array.reshape(array.shape[:2])
            img = Image.fromarray(array, mode='L')
            if field_type == L_FIELD:
                img = img.resize((x / 2 for x in img.size), Image.LANCZOS)
            img.save(buffer, extension)
        else:
            extension = 'png'
            channels = ('R', 'G', 'B', 'A') if field_type == RGBA_FIELD else ('R', 'G', 'B')
            if array.shape[2] == 1:
                channels = ['L']
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
        np.save(buffer, texture_arr)
        buffer.flush()
        filename = "%s.npy" % texture.texture.name
        texture.cache.save(filename, ContentFile(buffer.getvalue()), save=False)
