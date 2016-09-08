from time import time

from django.core.exceptions import ObjectDoesNotExist
from PIL import Image, ImageChops
import numpy as np

from lazy import lazy

from .base import BaseShirtBuilder
from processing.male_configs import models
from processing.rendering.compose import Composer
from processing.models import PROJECTION
from processing.rendering.compose import ImageConf
from backend.models import ContrastDetails

from dictionaries import models as dictionaries


class MaleShirtBuilder(BaseShirtBuilder):
    def _setup(self):
        super(MaleShirtBuilder, self)._setup()
        self.collar_buttons = dictionaries.CollarButtons.objects.get(pk=self.collar['size']).buttons

    @lazy
    def collar_conf(self):
        try:
            collar_conf = models.MaleCollarConfiguration.objects.prefetch_related('masks').get(
                collar_id=self.collar['type'],
                buttons=self.collar_buttons)
            return collar_conf
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Collar configuration not found for given parameters: %s" % self.collar)

    @lazy
    def cuff_conf(self):
        try:
            cuff_conf = models.MaleCuffConfiguration.objects.get(cuff_types__id=self.cuff['type'] if self.cuff else None,
                                                              rounding_id=self.cuff['rounding'] if self.cuff else None)
            return cuff_conf
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Collar configuration not found for given parameters: %s" % self.collar)


    def append_dickey(self):
        if self.projection == PROJECTION.back or not self.dickey:
            return None
        start = time()
        conf = self.get_compose_configuration(models.DickeyConfiguration, {
            'dickey_id': self.dickey['type'],
            'hem_id': self.hem
        })
        self.cache_builder.create_cache(conf, ('light', 'uv'), resolution=self.resolution)
        self.cache_builder.create_cache(self.cuff_conf, ('side_mask',), resolution=self.resolution)
        light = conf.cache.get(source_field='light', resolution=self.resolution)
        alpha = conf.cache.get(source_field='uv_alpha', resolution=self.resolution)
        alpha_img = Image.open(alpha.file.path)
        dickey_alphas = []
        for alpha_cache in self.alphas:
            if isinstance(alpha_cache.content_object.content_object, models.MaleCollarConfiguration) or \
                    isinstance(alpha_cache.content_object.content_object, models.MaleCuffConfiguration):
                dickey_alphas.append(alpha_cache)
        if self.projection == PROJECTION.side and self.sleeve.cuffs:
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
        self._setup()
        total = time()
        start = time()
        texture = self.get_fabric_texture(self.fabric)
        self.cache_builder.cache_texture(texture)
        self.append_model(self.get_compose_configuration(models.MaleBodyConfiguration, {
            'sleeve_id': self.sleeve.id,
            'hem_id': self.hem,
            'cuff_types__id': self.cuff['type'] if self.cuff else None
        }))
        self.append_contrasting_part(self.collar_conf, self.collar_model, ContrastDetails.COLLAR_ELEMENTS)
        if self.sleeve.cuffs:
            self.append_contrasting_part(self.cuff_conf, self.cuff_model, ContrastDetails.CUFF_ELEMENTS)
        self.append_model(self.get_compose_configuration(models.MalePocketConfiguration, {
            'pocket_id': self.pocket
        }))
        self.append_model(self.get_back())
        self.append_model(self.get_compose_configuration(models.MalePlacketConfiguration, {
            'plackets': self.placket.id,
            'hem_id': self.hem
        }), post_shadow=True)
        if self.projection == PROJECTION.back and self.yoke:
            self.append_model(self.get_compose_configuration(models.MaleYokeConfiguration, {
                'yoke_id': self.yoke
            }))

        if self.projection != PROJECTION.back and self.placket.show_buttons:
            buttons_conf = self.get_buttons_conf(models.MaleBodyButtonsConfiguration, {})
            self.append_buttons_stitches(buttons_conf)

        if self.cuff and self.sleeve.cuffs:
            self.append_buttons_stitches(self.get_buttons_conf(models.MaleCuffButtonsConfiguration, {
                'cuff_id': self.cuff['type'],
                'rounding_types__id': self.cuff['rounding']
            }))

        self.append_buttons_stitches(self.get_buttons_conf(models.MaleCollarButtonsConfiguration, {
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
        if self.initials:
            self.add_initials(res, self.initials, self.resolution, self.pocket)

        print("compose", time() - start)
        print("total", time() - total)

        return res

    def get_back(self):
        if not self.back:
            return None
        back_conf = models.MaleBackConfiguration.objects.get(back_id=self.back, tuck_id=self.tuck, hem_id=self.hem)
        return back_conf.sources.filter(projection=self.projection).first()

    @classmethod
    def get_initials_configuration(cls, initials, pocket):
        if not initials:
            return

        configurations = models.MaleInitialsConfiguration.objects.filter(
            font_id=initials['font'], location=initials['location'], pocket=pocket
        ).select_related('font')
        return configurations.first()