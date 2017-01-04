from io import BytesIO
from math import floor, ceil

import numpy as np
from PIL import Image
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from scipy import ndimage

from core.settings.base import RENDER
from processing.female_configs.models import FemaleBodyConfiguration
from processing.male_configs.models import MaleBodyConfiguration
from processing.models import SourceCache, CACHE_RESOLUTION, PROJECTION, CuffConfiguration, ButtonsSource
from processing.rendering.compose import apply_srgb
from processing.rendering.utils import Matrix, Submatrix, exr_to_array, image_from_array, scale_tuple
from .rendering.utils import gamma

EXR_FIELD = 'EXR'
RGBA_FIELD = 'RGBA'
L_FIELD = 'L'
STITCHES = 'S'


def is_base_layer(model):
    content_object = getattr(model, 'content_object', None)
    is_body = isinstance(content_object, FemaleBodyConfiguration) or isinstance(content_object, MaleBodyConfiguration)
    is_cuffs = isinstance(content_object, CuffConfiguration)
    is_back_cuffs = is_cuffs and model.projection == PROJECTION.back
    return is_body or is_back_cuffs


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
        'side_mask': L_FIELD,
        'shadow': RGBA_FIELD
    }

    @staticmethod
    def create_cache(instance, fields, resolution, field_types=None):
        matrices = []
        field_types = field_types or CacheBuilder.DEFAULT_FIELD_TYPES
        preview_scale = RENDER["preview_scale"]
        is_preview = resolution == CACHE_RESOLUTION.preview
        crop = RENDER['crop_scale']
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
                array[..., 0] *= size[0] - 1
                array[..., 1] *= size[1] - 1

                w = (crop[0] * size[1], crop[1] * size[0],
                     crop[2] * size[1], crop[3] * size[0])
                array = array[w[1]:w[3], w[0]:w[2]]

                alpha = image_from_array(array[..., 3])
                alpha_scale = preview_scale / 2.0 if is_preview else 0.5
                alpha = alpha.resize(scale_tuple(alpha.size, alpha_scale), Image.LANCZOS)
                alpha_array = np.asarray(alpha).astype('float32') / 255.0
                matrices.append(('uv_alpha', Submatrix(alpha_array), CacheBuilder.SCALE_MAP['uv'] / 2.0))

                if is_preview:
                    array = ndimage.zoom(array, [preview_scale, preview_scale, 1], order=0)

            else:
                img = image_from_array(array)
                field_type = field_types.get(field) or CacheBuilder.DEFAULT_FIELD_TYPES.get(field)
                w = (
                    img.size[0] * crop[0], img.size[1] * crop[1],
                    img.size[0] * crop[2], img.size[1] * crop[3],
                )
                img = img.crop(w)

                # fix for buttons brightness
                if isinstance(instance, ButtonsSource) and field == 'image':
                    img = apply_srgb(img)

                if field_type == L_FIELD or is_preview:
                    resize_factor = preview_scale if is_preview else 1
                    if field_type == L_FIELD:
                        resize_factor /= 2.0
                    img = img.resize(scale_tuple(img.size, resize_factor), Image.LANCZOS)

                array = np.asarray(img).astype('float32') / 255.0

            if is_base_layer(instance):
                matrix = Matrix(array)
            else:
                try:
                    matrix = Submatrix(array)
                except:
                    print(image.path)
                    raise

            if field == 'uv':
                matrix._source = matrix._source[..., :2].astype('uint16')  # cut redundant channels from uv

            scale = CacheBuilder.SCALE_MAP.get(field, 1)
            matrices.append((field, matrix, scale))

        if not matrices:
            print("Failed to cache source: fields %s are not found; source id: %s" % (fields, instance.id))
            return

        size_array = []
        for _, matrix, scale in matrices:
            size_array.append([floor(x / scale) if i < 2 else ceil(x / scale) for i, x in enumerate(matrix.bbox)])

        (x0, y0, x1, y1) = zip(*size_array)

        bbox = (min(x0), min(y0), max(x1), max(y1))

        for field, matrix, scale in matrices:
            # remove old cache
            instance.cache.filter(source_field=field, resolution=resolution).delete()
            scaled_bbox = scale_tuple(bbox, scale)
            matrix.repick(scaled_bbox)
            field_type = field_types.get(field) or CacheBuilder.DEFAULT_FIELD_TYPES.get(field)
            (buffer, extension) = CacheBuilder.get_buffer(matrix.values, field_type)
            filename = "%s_%s_%s.%s" % (instance._meta.model_name, instance.id, field, extension)
            position = scaled_bbox[:2][::-1]
            ct = ContentType.objects.get_for_model(instance)
            cache = SourceCache(source_field=field, resolution=resolution, object_id=instance.id, content_type=ct,
                                position=position)
            cache.file.save(filename, ContentFile(buffer.getvalue()))

    @staticmethod
    def get_buffer(array, field_type):
        buffer = BytesIO()
        if field_type == EXR_FIELD:
            extension = 'npy'
            np.save(buffer, array)
        elif field_type == L_FIELD or field_type == STITCHES:
            extension = 'png'
            array = (array * 255.0).astype('uint8')
            if len(array.shape) > 2:
                if array.shape[2] > 1:
                    array = array[..., -1]  # only take alpha
                array = array.reshape(array.shape[:2])
            img = Image.fromarray(array, mode='L')
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

        filename = "%s.npy" % texture.texture.name
        ct = ContentType.objects.get_for_model(texture)
        SourceCache.objects.filter(object_id=texture.id, content_type=ct).delete()

        def save_to_cache(image, resolution):
            texture_arr = np.asarray(image).transpose(1, 0, 2)
            buffer = BytesIO()
            np.save(buffer, texture_arr)
            buffer.flush()
            cache = SourceCache(source_field='texture', resolution=resolution, object_id=texture.id, content_type=ct,
                                position=(0, 0))
            cache.file.save(filename, ContentFile(buffer.getvalue()))

        img = Image.open(texture.texture.path)

        if texture.gamma_correction:
            img = gamma(img)

        save_to_cache(img, CACHE_RESOLUTION.preview)
