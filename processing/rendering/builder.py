from time import time

from PIL import Image, ImageOps
import numpy as np
from django.db.models import ObjectDoesNotExist
from django.db.models import Q

from backend.models import ContrastDetails
from backend.models import Fabric
from dictionaries import models as dictionaries
import processing.models as compose
from processing.rendering.compose import Composer, ImageConf

from lazy import lazy


class ShirtBuilder(object):
    def __init__(self, shirt_data, projection):
        self.projection = projection
        self.shirt_data = shirt_data
        self.collar = shirt_data.get('collar')
        self.collar_buttons = dictionaries.CollarButtons.objects.get(pk=self.collar['size']).buttons
        self.pocket = shirt_data.get('pocket')
        self.cuff = shirt_data.get('cuff')
        self.custom_buttons_type = shirt_data.get('custom_buttons_type')
        self.custom_buttons = shirt_data.get('custom_buttons')
        self.sleeve = dictionaries.SleeveType.objects.get(pk=shirt_data.get('sleeve'))
        self.hem = shirt_data.get('hem')
        self.placket = shirt_data.get('placket')
        self.tuck = shirt_data.get('tuck')
        self.back = shirt_data.get('back')
        self.dickey = shirt_data.get('dickey')
        self.fabric = shirt_data.get('fabric')
        self.yoke = shirt_data.get('yoke')
        self.contrast_details = shirt_data.get('contrast_details')
        self.reset()

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
        return fabric.texture

    @lazy
    def collar_conf(self):
        return compose.CollarConfiguration.objects.prefetch_related('masks').get(collar_id=self.collar['type'],
                                                                                 buttons=self.collar_buttons)

    @lazy
    def collar_model(self):
        return self.collar_conf.sources.filter(projection=self.projection).first()

    @lazy
    def cuff_conf(self):
        return compose.CuffConfiguration.objects.get(cuff_types__id=self.cuff['type'] if self.cuff else None,
                                                     rounding_id=self.cuff['rounding'] if self.cuff else None)

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
        light = conf.cache.get(source_field='light')
        alpha = conf.cache.get(source_field='uv_alpha')
        alpha_img = Image.open(alpha.file.path)
        dickey_alphas = []
        for alpha_cache in self.alphas:
            if isinstance(alpha_cache.content_object.content_object, compose.CollarConfiguration) or \
                    isinstance(alpha_cache.content_object.content_object, compose.CuffConfiguration):
                dickey_alphas.append(alpha_cache)
        if self.projection == compose.PROJECTION.side:
            dickey_alphas.append(self.cuff_conf.cache.get(source_field='side_mask'))
        for alpha_cache in dickey_alphas:
            part_alpha = Image.open(alpha_cache.file.path)
            inverted = ImageOps.invert(part_alpha)
            alpha_img.paste(inverted,
                            (
                                alpha_cache.position[0] - alpha.position[0],
                                alpha_cache.position[1] - alpha.position[1]
                            ),
                            mask=part_alpha)
        texture = self.get_fabric_texture(self.dickey['fabric'])
        dickey = Composer.create(
            texture=texture.cache.path,
            uv=np.load(conf.cache.get(source_field='uv').file.path),
            light=Image.open(light.file.path),
            alpha=alpha_img
        )
        print("dickey", time() - start)
        return ImageConf(dickey, light.position)


    def build_shirt(self):
        total = time()
        start = time()
        texture = self.get_fabric_texture(self.fabric)

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
            'placket_id': self.placket,
            'hem_id': self.hem
        }), post_shadow=True)

        if self.projection == compose.PROJECTION.back:
            self.append_model(self.get_compose_configuration(compose.YokeConfiguration, {
                'yoke_id': self.yoke
            }))

        if self.projection != compose.PROJECTION.back:
            self.append_buttons_stitches(self.get_buttons_conf(compose.BodyButtonsConfiguration, {
                'buttons_id': self.custom_buttons_type
            }))

        if self.cuff:
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
            texture=texture.cache.path,
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
        self.uv.append(model.cache.get(source_field='uv'))
        try:
            self.lights.append(model.cache.get(source_field='light'))
        except ObjectDoesNotExist:
            pass
        try:
            shadow = model.cache.get(source_field='ao')
            if post_shadow:
                self.post_shadows.append(ImageConf.for_cache(shadow))
            else:
                self.shadows.append(shadow)
        except ObjectDoesNotExist:
            pass
        self.alphas.append(model.cache.get(source_field='uv_alpha'))

    def append_stitches(self, stitches):
        for conf in stitches:
            try:
                cache = conf.cache.get(source_field='image')
            except Exception as e:
                print(e.message)
                continue

            image = {
                'image': cache.file.path,
                'position': cache.position
            }
            if conf.type == compose.StitchesSource.STITCHES_TYPE.under:
                self.lower_stitches.append(ImageConf.for_cache(cache))
            else:
                self.upper_stitches.append(ImageConf.for_cache(cache))

    def append_buttons(self, conf):
        if conf is None:
            return
        try:
            buttons_cache = conf.cache.get(source_field='image')
        except Exception as e:
            print(e.message)
            return
        ao = conf.cache.filter(source_field='ao').first()
        if conf.projection == compose.PROJECTION.front or not isinstance(conf.content_object,
                                                                         compose.BodyButtonsConfiguration):
            self.buttons.append(ImageConf.for_cache(buttons_cache))
            if ao:
                self.post_shadows.append(ImageConf.for_cache(ao))

        else:
            buttons_base = Image.new("RGBA", (2048, 2048), 0)
            img = Image.open(buttons_cache.file.path)
            buttons_base.paste(img, buttons_cache.position, mask=img)
            if ao:
                shadow = Image.open(ao.file.path)
                buttons_base.paste(shadow, ao.position, mask=shadow)
            self.base_layer.append(buttons_base)

    def get_compose_configuration(self, model, filters):
        filters = map(lambda (k, v): Q(**{k: v}) | Q(**{"%s__isnull" % k: True}), filters.iteritems())
        try:
            configuration = model.objects.get(*filters)
            return configuration.sources.filter(projection=self.projection).first()
        except ObjectDoesNotExist:
            return None

    def get_back(self):
        back_conf = compose.BackConfiguration.objects.get(back_id=self.back, tuck=self.tuck, hem_id=self.hem)
        return back_conf.sources.filter(projection=self.projection).first()

    def get_buttons_conf(self, model, filters):
        filters = map(lambda (k, v): Q(**{k: v}) | Q(**{"%s__isnull" % k: True}), filters.iteritems())
        try:
            configuration = model.objects.get(*filters)
            return (configuration.sources.filter(projection=self.projection).first(),
                    configuration.stitches.filter(projection=self.projection))
        except ObjectDoesNotExist:
            print('not found: %s' % model._meta.verbose_name)
            print('params: %s' % filters)
            return None

    def append_solid_contrasting_part(self, ao, light_conf, model, part_details, uv):
        fabric = part_details[0]['fabric']
        texture = self.get_fabric_texture(fabric)
        alpha_cache = model.cache.get(source_field='uv_alpha')
        self.alphas.append(alpha_cache)
        composed_detail = Composer.create(
            texture=texture.cache.path,
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
            alpha_cache = mask.cache.get(source_field='mask')
            alpha = Image.new("L", light_image.size, color=0)
            alpha_image = Image.open(alpha_cache.file.path)
            position = tuple(alpha_cache.position[x] - light_conf.position[x] for x in [0, 1])
            alpha.paste(alpha_image, position)
            composed_detail = Composer.create(
                texture.cache.path,
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
        uv = np.load(model.cache.get(source_field='uv').file.path)
        light_conf = model.cache.get(source_field='light')
        ao = model.cache.get(source_field='ao').file.path
        fabrics = set(map(lambda d: d['fabric'], part_details))
        if sorted(present_part_keys) == sorted(part_keys) and len(fabrics) == 1:
            self.append_solid_contrasting_part(ao, light_conf, model, part_details, uv)
        else:
            self.append_model(model)
            detail_masks = []
            for detail in part_details:
                mask = conf.masks.filter(element=detail['element'], projection=self.projection).first()
                if mask:
                    detail_masks.append((detail, mask))

            if detail_masks:
                self.append_granular_contrasting_part(ao, detail_masks, light_conf, uv)
