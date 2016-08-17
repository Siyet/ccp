from time import time

from PIL import Image, ImageChops, ImageColor
import numpy as np
from django.db.models import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from lazy import lazy

from backend.models import ContrastDetails, Fabric, CustomButtons
from dictionaries import models as dictionaries
import processing.models as compose
from processing.rendering.compose import Composer, ImageConf
from core.utils import first
from .utils import hex_to_rgb, scale_tuple
from core.settings.base import RENDER
from processing.cache import CacheBuilder


class CacheBuilderMock(object):
    @staticmethod
    def cache_texture(*args, **kwargs):
        pass

    @staticmethod
    def create_cache(*args, **kwargs):
        pass


cache_builder = CacheBuilderMock
# cache_builder = CacheBuilder


class ShirtBuilder(object):
    def __init__(self, shirt_data, projection, resolution=compose.CACHE_RESOLUTION.full):
        self.resolution = resolution
        self.projection = projection
        self.collar = self.extract(shirt_data, 'collar')
        self.collar_buttons = dictionaries.CollarButtons.objects.get(pk=self.collar['size']).buttons
        self.pocket = self.extract(shirt_data, 'pocket')
        self.cuff = self.extract(shirt_data, 'cuff')
        self.custom_buttons_type = self.extract(shirt_data, 'custom_buttons_type')
        self.custom_buttons = self.extract(shirt_data, 'custom_buttons')
        self.sleeve = dictionaries.SleeveType.objects.get(pk=shirt_data.get('sleeve'))
        self.hem = self.extract(shirt_data, 'hem')
        self.placket = self.extract(shirt_data, 'placket')
        if self.placket:
            self.placket = dictionaries.PlacketType.objects.get(pk=self.placket)
        self.tuck = shirt_data.get('tuck', False)
        self.back = self.extract(shirt_data, 'back')
        self.dickey = self.extract(shirt_data, 'dickey')
        self.fabric = shirt_data.get('fabric')
        self.yoke = self.extract(shirt_data, 'yoke')
        self.contrast_details = shirt_data.get('contrast_details', [])
        self.contrast_stitches = shirt_data.get('contrast_stitches', [])
        self.reset()

    def extract(self, data, param):
        value = data.get(param, None)
        if isinstance(value, dict):
            for k in value.keys():
                value[k] = self.extract(value, k)
        return value or None  # skip empty strings

    def reset(self):
        self.uv = []
        self.lights = []
        self.shadows = []
        self.post_shadows = []
        self.alphas = []
        self.buttons = []
        self.lower_stitches = []
        self.upper_stitches = []
        self.base_layer = []
        self.extra_details = []

    def get_fabric_texture(self, fabric_id):
        fabric = Fabric.objects.select_related('texture').get(pk=fabric_id)
        cache_builder.cache_texture(fabric.texture)
        return fabric.texture

    @lazy
    def buttons_color(self):
        if self.custom_buttons and self.custom_buttons_type:
            buttons = CustomButtons.objects.filter(pk=self.custom_buttons).first()
            if buttons:
                return ImageColor.getrgb(buttons.color) + (255,)

        return None

    @lazy
    def collar_conf(self):
        try:
            collar_conf = compose.CollarConfiguration.objects.prefetch_related('masks').get(
                collar_id=self.collar['type'],
                buttons=self.collar_buttons)
            return collar_conf
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Collar configuration not found for given parameters: %s" % self.collar)

    @lazy
    def collar_model(self):
        return self.collar_conf.sources.filter(projection=self.projection).first()

    @lazy
    def cuff_conf(self):
        try:
            cuff_conf = compose.CuffConfiguration.objects.get(cuff_types__id=self.cuff['type'] if self.cuff else None,
                                                              rounding_id=self.cuff['rounding'] if self.cuff else None)
            return cuff_conf
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Collar configuration not found for given parameters: %s" % self.collar)

    @lazy
    def cuff_model(self):
        return self.cuff_conf.sources.filter(projection=self.projection).first()

    def append_dickey(self):
        if self.projection == compose.PROJECTION.back or not self.dickey:
            return None
        start = time()
        conf = self.get_compose_configuration(compose.DickeyConfiguration, {
            'dickey_id': self.dickey['type'],
            'hem_id': self.hem
        })
        cache_builder.create_cache(conf, ('light', 'uv'), resolution=self.resolution)
        cache_builder.create_cache(self.cuff_conf, ('side_mask',), resolution=self.resolution)
        light = conf.cache.get(source_field='light', resolution=self.resolution)
        alpha = conf.cache.get(source_field='uv_alpha', resolution=self.resolution)
        alpha_img = Image.open(alpha.file.path)
        dickey_alphas = []
        for alpha_cache in self.alphas:
            if isinstance(alpha_cache.content_object.content_object, compose.CollarConfiguration) or \
                    isinstance(alpha_cache.content_object.content_object, compose.CuffConfiguration):
                dickey_alphas.append(alpha_cache)
        if self.projection == compose.PROJECTION.side and self.sleeve.cuffs:
            dickey_alphas.append(self.cuff_conf.cache.get(source_field='side_mask', resolution=self.resolution))
        for alpha_cache in dickey_alphas:
            part_alpha = Image.open(alpha_cache.file.path)
            part_position = alpha_cache.position
            part_layer = Image.new(alpha_img.mode, alpha_img.size)
            part_layer.paste(part_alpha, (
                part_position[0] - alpha.position[0],
                part_position[1] - alpha.position[1]
            ))
            alpha_img = ImageChops.subtract(alpha_img, part_layer)

        texture = self.get_fabric_texture(self.dickey['fabric'])
        dickey = Composer.create_dickey(
            texture=texture.cache.get(resolution=self.resolution).file.path,
            uv=np.load(conf.cache.get(source_field='uv', resolution=self.resolution).file.path),
            alpha=alpha_img
        )
        print("dickey", time() - start)
        return ImageConf(dickey, light.position)

    def build_shirt(self):
        total = time()
        start = time()
        texture = self.get_fabric_texture(self.fabric)
        cache_builder.cache_texture(texture)
        self.append_model(self.get_compose_configuration(compose.BodyConfiguration, {
            'sleeve_id': self.sleeve.id,
            'hem_id': self.hem,
            'cuff_types__id': self.cuff['type'] if self.cuff else None
        }))
        self.append_contrasting_part(self.collar_conf, self.collar_model, ContrastDetails.COLLAR_ELEMENTS)
        if self.sleeve.cuffs:
            self.append_contrasting_part(self.cuff_conf, self.cuff_model, ContrastDetails.CUFF_ELEMENTS)
        self.append_model(self.get_compose_configuration(compose.PocketConfiguration, {
            'pocket_id': self.pocket
        }))
        self.append_model(self.get_back())
        self.append_model(self.get_compose_configuration(compose.PlacketConfiguration, {
            'plackets': self.placket.id,
            'hem_id': self.hem
        }), post_shadow=True)
        if self.projection == compose.PROJECTION.back and self.yoke:
            self.append_model(self.get_compose_configuration(compose.YokeConfiguration, {
                'yoke_id': self.yoke
            }))

        if self.projection != compose.PROJECTION.back and self.placket.show_buttons:
            buttons_conf = self.get_buttons_conf(compose.BodyButtonsConfiguration, {})
            self.append_buttons_stitches(buttons_conf)

        if self.cuff and self.sleeve.cuffs:
            self.append_buttons_stitches(self.get_buttons_conf(compose.CuffButtonsConfiguration, {
                'cuff_id': self.cuff['type'],
                'rounding_types__id': self.cuff['rounding']
            }))

        self.append_buttons_stitches(self.get_buttons_conf(compose.CollarButtonsConfiguration, {
            'collar_id': self.collar['type'],
            'buttons': self.collar_buttons
        }))

        uv = Composer.compose_uv(self.uv)
        light = Composer.compose_light(self.lights)
        if texture.needs_shadow:
            shadow = Composer.compose_light(self.shadows)
        else:
            shadow = None
        alpha = Composer.compose_alpha(self.alphas)
        dickey = self.append_dickey()
        print("preparation", time() - start)
        start = time()

        res = Composer.create(
            texture=texture.cache.get(resolution=self.resolution).file.path,
            uv=uv,
            light=light,
            shadow=shadow,
            post_shadows=self.post_shadows,
            alpha=alpha,
            buttons=self.buttons,
            lower_stitches=self.lower_stitches,
            upper_stitches=self.upper_stitches,
            dickey=dickey,
            extra_details=self.extra_details,
            base_layer=self.base_layer
        )

        print("compose", time() - start)
        print("total", time() - total)

        return res

    def append_buttons_stitches(self, conf):
        if conf is None:
            return

        (buttons, stitches) = conf
        self.append_buttons(buttons)
        self.append_stitches(stitches)

    def append_model(self, model, post_shadow=False):

        if model is None:
            return
        cache_builder.create_cache(model, ('uv', 'light', 'ao'), resolution=self.resolution)
        self.uv.append(model.cache.get(source_field='uv', resolution=self.resolution))
        try:
            self.lights.append(model.cache.get(source_field='light', resolution=self.resolution))
        except ObjectDoesNotExist:
            pass
        try:
            shadow = model.cache.get(source_field='ao', resolution=self.resolution)
            if post_shadow:
                self.post_shadows.append(ImageConf.for_cache(shadow))
            else:
                self.shadows.append(shadow)
        except ObjectDoesNotExist:
            pass
        self.alphas.append(model.cache.get(source_field='uv_alpha', resolution=self.resolution))

    def append_stitches(self, stitches):
        if not self.contrast_stitches:
            return

        for conf in stitches:
            try:
                cache_builder.create_cache(stitches, ('image',), resolution=self.resolution)
                cache = conf.cache.get(source_field='image', resolution=self.resolution)
            except Exception as e:
                print(e.message)
                continue

            stitches_conf = ImageConf.for_cache(cache)

            ct = ContentType.objects.get_for_model(conf.content_object)

            relation = compose.StitchColor.objects.get(content_type_id=ct.id)
            element = relation.element_id
            element_info = first(lambda s: s['element'] == element, self.contrast_stitches)
            image = Image.open(cache.file.path)
            if image.mode == 'L' and element_info:
                color = dictionaries.StitchColor.objects.get(pk=element_info["color"])
                back = Image.new('RGB', image.size, hex_to_rgb(color.color))
                back.putalpha(image)
                stitches_conf.image = back

            if conf.type == compose.StitchesSource.STITCHES_TYPE.under:
                self.lower_stitches.append(stitches_conf)
            else:
                self.upper_stitches.append(stitches_conf)

    def append_buttons(self, conf):
        if conf is None:
            return
        try:
            cache_builder.create_cache(conf, ('image', 'ao'), resolution=self.resolution)
            buttons_cache = conf.cache.get(source_field='image', resolution=self.resolution)
        except Exception as e:
            print(e.message)
            return
        ao = conf.cache.filter(source_field='ao', resolution=self.resolution).first()
        buttons_image = Image.open(buttons_cache.file.path)
        if self.buttons_color:
            color_layer = Image.new("RGBA", buttons_image.size, color=self.buttons_color)
            buttons_image = ImageChops.multiply(buttons_image, color_layer)

        if conf.projection == compose.PROJECTION.side and isinstance(conf.content_object,
                                                                     compose.BodyButtonsConfiguration):
            scale = 1.0 if self.resolution == compose.CACHE_RESOLUTION.full else RENDER['preview_scale']
            size = scale_tuple(RENDER['default_size'], scale)
            buttons_base = Image.new("RGBA", size, 0)
            buttons_base.paste(buttons_image, buttons_cache.position, mask=buttons_image)
            if ao:
                shadow = Image.open(ao.file.path)
                buttons_base.paste(shadow, ao.position, mask=shadow)
            self.base_layer.append(buttons_base)
        else:
            self.buttons.append(ImageConf(image=buttons_image, position=buttons_cache.position))
            if ao:
                self.post_shadows.append(ImageConf.for_cache(ao))

    def get_compose_configuration(self, model, filters):
        filters = map(lambda (k, v): Q(**{k: v}) | Q(**{"%s__isnull" % k: True}), filters.iteritems())
        try:
            configuration = model.objects.get(*filters)
            return configuration.sources.filter(projection=self.projection).first()
        except ObjectDoesNotExist:
            return None

    def get_back(self):
        if not self.back:
            return None
        back_conf = compose.BackConfiguration.objects.get(back_id=self.back, tuck=self.tuck, hem_id=self.hem)
        return back_conf.sources.filter(projection=self.projection).first()

    def get_buttons_conf(self, model, filters):
        filters = map(lambda (k, v): Q(**{k: v}) | Q(**{"%s__isnull" % k: True}), filters.iteritems())

        configuration = model.objects.filter(*filters).first()
        if not configuration:
            print('not found: %s' % model._meta.verbose_name)
            print('params: %s' % filters)
            return None

        return (configuration.sources.filter(projection=self.projection).first(),
                configuration.stitches.filter(projection=self.projection))

    def append_solid_contrasting_part(self, ao, light_conf, model, fabric, uv):
        texture = self.get_fabric_texture(fabric)
        alpha_cache = model.cache.get(source_field='uv_alpha', resolution=self.resolution)
        self.alphas.append(alpha_cache)
        composed_detail = Composer.create(
            texture=texture.cache.get(resolution=self.resolution).file.path,
            uv=uv,
            light=Image.open(light_conf.file.path),
            shadow=Image.open(ao) if texture.needs_shadow else None,
            alpha=Image.open(alpha_cache.file.path)
        )
        self.extra_details.append(ImageConf(composed_detail, light_conf.position))

    def append_granular_contrasting_part(self, ao, detail_masks, light_conf, uv):
        light_image = Image.open(light_conf.file.path)
        ao = Image.open(ao)
        for detail_mask in detail_masks:
            detail, mask = detail_mask
            fabric = detail['fabric']
            texture = self.get_fabric_texture(fabric)
            alpha_cache = mask.cache.get(source_field='mask', resolution=self.resolution)
            alpha = Image.new("L", light_image.size, color=0)
            alpha_image = Image.open(alpha_cache.file.path)
            position = tuple(alpha_cache.position[x] - light_conf.position[x] for x in [0, 1])
            alpha.paste(alpha_image, position)
            composed_detail = Composer.create(
                texture.cache.get(resolution=self.resolution).file.path,
                uv,
                light_image,
                ao if texture.needs_shadow else None,
                alpha=alpha
            )
            self.extra_details.append(ImageConf(composed_detail, light_conf.position))

    def append_contrasting_part(self, conf, model, elements):
        if not self.contrast_details:
            return self.append_model(model)

        part_keys = set([x[0] for x in elements])
        all_detail_keys = set([x['element'] for x in self.contrast_details])
        if not all_detail_keys.intersection(part_keys):
            return self.append_model(model)
        present_part_keys = filter(lambda k: k in part_keys, all_detail_keys)
        part_details = filter(lambda k: k['element'] in part_keys, self.contrast_details)
        cache_builder.create_cache(model, ('uv', 'light', 'ao'), resolution=self.resolution)
        uv = np.load(model.cache.get(source_field='uv', resolution=self.resolution).file.path)
        light_conf = model.cache.get(source_field='light', resolution=self.resolution)
        ao = model.cache.get(source_field='ao', resolution=self.resolution).file.path
        fabrics = set(map(lambda d: d['fabric'], part_details))
        if sorted(present_part_keys) == sorted(part_keys) and len(fabrics) == 1:
            self.append_solid_contrasting_part(ao, light_conf, model, fabrics.pop(), uv)
        else:
            self.append_model(model)
            detail_masks = []
            for detail in part_details:
                mask = conf.masks.filter(element=detail['element'], projection=self.projection).first()
                if mask:
                    cache_builder.create_cache(mask, ('mask',), resolution=self.resolution)
                    detail_masks.append((detail, mask))

            if detail_masks:
                self.append_granular_contrasting_part(ao, detail_masks, light_conf, uv)

            # for external cuff part there's no mask: we just replace whole manget
            else:
                cuff_element = first(lambda x: x['element'] == ContrastDetails.CUFF_ELEMENTS.cuff_outer, part_details)
                if cuff_element:
                    self.append_solid_contrasting_part(ao, light_conf, model, cuff_element['fabric'], uv)
