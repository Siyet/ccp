import numpy as np
from PIL import Image, ImageChops, ImageColor, ImageFont, ImageOps
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from django.db.models import Q
from django.utils.functional import cached_property

import processing.models as compose
from backend.models import ContrastDetails, Fabric, CustomButtons, Collection
from core.settings.base import RENDER
from core.utils import first
from dictionaries import models as dictionaries
from processing.cache import STITCHES
from processing.rendering.compose import Composer, ImageConf
from processing.rendering.utils import hex_to_rgb, cropped_box, draw_rotated_text
# noinspection PyUnresolvedReferences
from processing.cache import CacheBuilder


class CacheBuilderMock(object):
    @staticmethod
    def cache_texture(*args, **kwargs):
        CacheBuilder.cache_texture(*args, **kwargs)

    @staticmethod
    def create_cache(*args, **kwargs):
        pass


class BaseShirtBuilder(object):
    cache_builder = CacheBuilderMock
    # cache_builder = CacheBuilder

    def __init__(self, shirt_data, projection, resolution=compose.CACHE_RESOLUTION.full):
        self.is_ready = False
        self.shirt_data = shirt_data
        self.resolution = resolution
        self.projection = projection

    def _setup(self):
        shirt_data = self.shirt_data
        self.collection_id = shirt_data['collection']
        self.collar = self.extract(shirt_data, 'collar')
        self.collar_buttons = dictionaries.CollarButtons.objects.get(pk=self.collar['size']).buttons
        self.pocket = self.extract(shirt_data, 'pocket')
        self.cuff = self.extract(shirt_data, 'cuff')
        self.clasp = self.extract(shirt_data, 'clasp', False)
        self.custom_buttons_type = self.extract(shirt_data, 'custom_buttons_type')
        self.custom_buttons = self.extract(shirt_data, 'custom_buttons')
        self.sleeve = dictionaries.SleeveType.objects.get(pk=shirt_data.get('sleeve'))
        self.hem = self.extract(shirt_data, 'hem')
        self.placket = self.extract(shirt_data, 'placket')
        if self.placket:
            self.placket = dictionaries.PlacketType.objects.get(pk=self.placket)
        self.tuck = self.extract(shirt_data, 'tuck')
        self.back = self.extract(shirt_data, 'back')
        self.dickey = self.extract(shirt_data, 'dickey')
        self.fabric = shirt_data.get('fabric')
        self.yoke = self.extract(shirt_data, 'yoke')
        self.contrast_details = shirt_data.get('contrast_details', [])
        self.contrast_stitches = shirt_data.get('contrast_stitches', [])
        self.initials = shirt_data.get('initials', None)
        self.reset()

    def extract(self, data, param, default=None):
        value = data.get(param, None)
        if isinstance(value, dict):
            for k in value.keys():
                value[k] = self.extract(value, k)
        return value or default  # skip empty strings

    def reset(self):
        self.uv = []
        self.lights = []
        self.ao = []
        self.shadows = []
        self.alphas = []
        self.buttons = []
        self.lower_stitches = []
        self.upper_stitches = []
        self.base_layer = []
        self.extra_details = []

    def compose_dickey(self):
        """
        Must be overriden in case dickey is necessary for model
        """
        return None

    def perform_compose(self):
        uv = Composer.compose_uv(self.uv)
        light = Composer.compose_ambience(self.lights)
        texture = self.get_fabric_texture(self.fabric)
        if texture.needs_shadow:
            ao = Composer.compose_ambience(self.ao)
        else:
            ao = None
        alpha = Composer.compose_alpha(self.alphas)

        dickey = self.compose_dickey()
        res = Composer.create(
            texture=texture.cache.get(resolution=self.resolution).file.path,
            uv=uv,
            light=light,
            ao=ao,
            shadows=self.shadows,
            alpha=alpha,
            buttons=self.buttons,
            lower_stitches=self.lower_stitches,
            upper_stitches=self.upper_stitches,
            dickey=dickey,
            extra_details=self.extra_details,
            base_layer=self.base_layer
        )

        if self.initials:
            self.add_initials(res, self.initials, self.resolution, self.pocket)

        self.reset()
        background = Image.new("RGBA", res.size, "white")
        return Image.alpha_composite(background, res)

    def get_fabric_texture(self, fabric):
        if not isinstance(fabric, Fabric):
            fabric = Fabric.objects.select_related('texture').get(pk=fabric)
        self.cache_builder.cache_texture(fabric.texture)
        return fabric.texture

    @cached_property
    def buttons_color(self):
        if self.custom_buttons and self.custom_buttons_type:
            buttons = CustomButtons.objects.filter(pk=self.custom_buttons).first()
            if buttons:
                return ImageColor.getrgb(buttons.color) + (255,)

        return None

    @cached_property
    def collection(self):
        return Collection.objects.get(pk=self.collection_id)

    @cached_property
    def collar_conf(self):
        raise NotImplementedError()

    @cached_property
    def collar_model(self):
        return self.collar_conf.sources.filter(projection=self.projection).first()

    @cached_property
    def cuff_conf(self):
        raise NotImplementedError()

    @cached_property
    def cuff_model(self):
        return self.cuff_conf.sources.filter(projection=self.projection).first()

    def append_buttons_stitches(self, conf):
        if conf is None:
            return

        (buttons, stitches) = conf
        self.append_buttons(buttons)
        self.append_stitches(stitches)

    def append_model(self, model, post_shadow=False):
        if model is None:
            return
        self.cache_builder.create_cache(model, ('uv', 'light', 'ao'), resolution=self.resolution)
        self.uv.append(model.cache.get(source_field='uv', resolution=self.resolution))
        try:
            self.lights.append(model.cache.get(source_field='light', resolution=self.resolution))
        except ObjectDoesNotExist:
            pass
        try:
            shadow = model.cache.get(source_field='ao', resolution=self.resolution)
            if post_shadow:
                self.shadows.append(ImageConf.for_cache(shadow))
            else:
                self.ao.append(shadow)
        except ObjectDoesNotExist:
            pass
        try:
            shadow = model.cache.get(source_field='shadow', resolution=self.resolution)
            self.shadows.append(ImageConf.for_cache(shadow))
        except ObjectDoesNotExist:
            pass
        self.alphas.append(model.cache.get(source_field='uv_alpha', resolution=self.resolution))

    def append_stitches(self, stitches):
        if not self.contrast_stitches:
            return

        for conf in stitches:
            try:
                self.cache_builder.create_cache(conf, ('image',), resolution=self.resolution,
                                                field_types={'image': STITCHES})
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
            self.cache_builder.create_cache(conf, ('image', 'ao'), resolution=self.resolution)
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
            box = cropped_box(RENDER['default_size'], RENDER['crop_scale'], scale)
            size = (box[2] - box[0], box[3] - box[1])
            buttons_base = Image.new("RGBA", size, 0)
            buttons_base.paste(buttons_image, buttons_cache.position, mask=buttons_image)
            if ao:
                shadow = Image.open(ao.file.path)
                buttons_base.paste(shadow, ao.position, mask=shadow)
            self.base_layer.append(buttons_base)
        else:
            self.buttons.append(ImageConf(image=buttons_image, position=buttons_cache.position))
            if ao:
                self.shadows.append(ImageConf.for_cache(ao))

    def get_compose_configuration(self, model, filters, source_filters=None):
        configurations = self.get_compose_configurations(model, filters, source_filters)
        return configurations.first() if configurations else None

    def filters_from_dict(self, filters):
        if filters:
            return [Q(**{k: v}) | Q(**{"%s__isnull" % k: True}) for k, v in filters.iteritems()]
        return []

    def get_compose_configurations(self, model, filters, source_filters=None):
        filters = self.filters_from_dict(filters)
        try:
            configuration = model.objects.get(*filters)
            sources = configuration.sources.filter(projection=self.projection)
            source_filters = self.filters_from_dict(source_filters)
            return sources.filter(*source_filters) if source_filters else sources

        except ObjectDoesNotExist:
            return None

    def get_buttons_conf(self, model, filters):
        filters = map(lambda (k, v): Q(**{k: v}) | Q(**{"%s__isnull" % k: True}), filters.iteritems())

        configuration = model.objects.filter(*filters).first()
        if not configuration:
            return None

        return (configuration.sources.filter(projection=self.projection).first(),
                configuration.stitches.filter(projection=self.projection))

    def append_solid_contrasting_part(self, ao, light_conf, model, fabric, uv):
        texture = self.get_fabric_texture(fabric)
        alpha_cache = model.cache.get(source_field='uv_alpha', resolution=self.resolution)
        self.alphas.append(alpha_cache)

        self.ao.append(ao)
        self.lights.append(light_conf)

        composed_detail = Composer.create(
            texture=texture.cache.get(resolution=self.resolution).file.path,
            uv=uv,
            alpha=Image.open(alpha_cache.file.path),
            srgb=False
        )

        self.extra_details.append(ImageConf(composed_detail, light_conf.position))

    def append_granular_contrasting_part(self, ao, detail_masks, light_conf, uv):
        light_image = Image.open(light_conf.file.path)
        for detail_mask in detail_masks:
            detail, mask = detail_mask
            fabric = detail['fabric']
            texture = self.get_fabric_texture(fabric)
            alpha_cache = mask.cache.get(source_field='mask', resolution=self.resolution)
            alpha = Image.new("L", light_image.size, color=0)
            alpha_image = Image.open(alpha_cache.file.path)
            position = tuple(ap - lp for ap, lp in zip(alpha_cache.position, light_conf.position))
            alpha.paste(alpha_image, position)
            composed_detail = Composer.create(
                texture.cache.get(resolution=self.resolution).file.path,
                uv,
                alpha=alpha,
                srgb=False
            )
            self.extra_details.append(ImageConf(composed_detail, light_conf.position))

    def append_contrasting_part(self, conf, model, elements):
        if self.contrast_details is None:
            return self.append_model(model)

        self.cache_builder.create_cache(model, ('uv', 'light', 'ao'), resolution=self.resolution)

        def sources_for(model):
            uv = np.load(model.cache.get(source_field='uv', resolution=self.resolution).file.path)
            light_conf = model.cache.get(source_field='light', resolution=self.resolution)
            ao = model.cache.get(source_field='ao', resolution=self.resolution).file.path
            return uv, light_conf, ao

        if not self.collection.contrast_details:
            (uv, light_conf, ao) = sources_for(model)
            self.append_solid_contrasting_part(ao, light_conf, model, self.collection.white_fabric, uv)
            return

        part_keys = set([x[0] for x in elements])
        all_detail_keys = set([x['element'] for x in self.contrast_details])
        if not all_detail_keys.intersection(part_keys):
            return self.append_model(model)
        present_part_keys = filter(lambda k: k in part_keys, all_detail_keys)
        part_details = filter(lambda k: k['element'] in part_keys, self.contrast_details)
        (uv, light_conf, ao) = sources_for(model)
        fabrics = set(map(lambda d: d['fabric'], part_details))
        if sorted(present_part_keys) == sorted(part_keys) and len(fabrics) == 1:
            self.append_solid_contrasting_part(ao, light_conf, model, fabrics.pop(), uv)
        else:
            self.append_model(model)
            detail_masks = []
            for detail in part_details:
                mask = conf.masks.filter(element=detail['element'], projection=self.projection).first()
                if mask:
                    self.cache_builder.create_cache(mask, ('mask',), resolution=self.resolution)
                    detail_masks.append((detail, mask))

            if detail_masks:
                self.append_granular_contrasting_part(ao, detail_masks, light_conf, uv)

            # for external cuff part there's no mask: we just replace whole manget
            else:
                cuff_element = first(lambda x: x['element'] == ContrastDetails.CUFF_ELEMENTS.cuff_outer, part_details)
                if cuff_element:
                    self.append_solid_contrasting_part(ao, light_conf, model, cuff_element['fabric'], uv)

    @classmethod
    def get_initials_configuration(cls, initials, pocket):
        raise NotImplementedError()

    @classmethod
    def add_initials(cls, image, initials, projection, pocket):
        if not initials:
            return
        if not initials['text']:
            return

        initials_configuration = cls.get_initials_configuration(initials, pocket)
        if not initials_configuration:
            return
        position = initials_configuration.positions.filter(projection=projection).first()
        if not position:
            return
        color = dictionaries.Color.objects.get(pk=initials['color'])
        color = hex_to_rgb(color.color)
        image_scale = float(image.size[0]) / RENDER['default_size'][0]
        font_size = int(round(image_scale * initials_configuration.font_size))
        font = ImageFont.truetype(initials_configuration.font.font.path, font_size, encoding='utf-8')
        text = draw_rotated_text(unicode(initials['text']), font, position.rotate)
        initials_position = (int(position.left * image.size[0]), int(position.top * image.size[1]))
        colorized_text = ImageOps.colorize(text, (0, 0, 0), color)
        image.paste(colorized_text, initials_position, text)
