from time import time

from django.core.exceptions import ObjectDoesNotExist
from PIL import Image, ImageChops
import numpy as np

from lazy import lazy

from .base import BaseShirtBuilder
from processing.female_configs import models
from processing.rendering.compose import Composer, ImageConf
from processing.models import PROJECTION
from backend.models import ContrastDetails

class FemaleShirtBuilder(BaseShirtBuilder):
    @lazy
    def collar_conf(self):
        try:
            collar_conf = models.FemaleCollarConfiguration.objects.prefetch_related('masks').get(
                collar_id=self.collar['type']
            )
            return collar_conf
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Collar configuration not found for given parameters: %s" % self.collar)

    @lazy
    def cuff_conf(self):
        try:
            cuff_conf = models.FemaleCuffConfiguration.objects.get(
                cuff_types__id=self.cuff['type'] if self.cuff else None,
                rounding_id=self.cuff['rounding'] if self.cuff else None
            )
            return cuff_conf
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Collar configuration not found for given parameters: %s" % self.collar)


    def build_shirt(self):
        self._setup()
        total = time()
        start = time()
        texture = self.get_fabric_texture(self.fabric)
        self.cache_builder.cache_texture(texture)

        body_models= self.get_compose_configurations(models.FemaleBodyConfiguration, {
            'sleeve_id': self.sleeve.id,
            'hem_id': self.hem,
            'cuff_types__id': self.cuff['type'] if self.cuff else None,
            'tuck_id': self.tuck,
        })
        if self.projection == PROJECTION.back:
            if self.sleeve.cuffs:
                self.append_contrasting_part(self.cuff_conf, self.cuff_model, ContrastDetails.CUFF_ELEMENTS)
            self.append_model(body_models.get(back_id=self.back))
        else:
            self.append_model(body_models.first())
            if self.sleeve.cuffs:
                self.append_contrasting_part(self.cuff_conf, self.cuff_model, ContrastDetails.CUFF_ELEMENTS)

        self.append_contrasting_part(self.collar_conf, self.collar_model, ContrastDetails.COLLAR_ELEMENTS)
        self.append_model(self.get_compose_configuration(models.FemalePocketConfiguration, {
            'pocket_id': self.pocket
        }))
        self.append_model(self.get_compose_configuration(models.FemalePlacketConfiguration, {
            'plackets': self.placket.id,
            'hem_id': self.hem,
            'tuck_id': self.tuck
        }), post_shadow=True)
        if self.projection == PROJECTION.back and self.yoke:
            self.append_model(self.get_compose_configuration(models.FemaleYokeConfiguration, {
                'yoke_id': self.yoke
            }))

        if self.projection != PROJECTION.back and self.placket.show_buttons:
            buttons_conf = self.get_buttons_conf(models.FemaleBodyButtonsConfiguration, {})
            self.append_buttons_stitches(buttons_conf)

        if self.cuff and self.sleeve.cuffs:
            self.append_buttons_stitches(self.get_buttons_conf(models.FemaleCuffButtonsConfiguration, {
                'cuff_id': self.cuff['type'],
                'rounding_types__id': self.cuff['rounding']
            }))

        self.append_buttons_stitches(self.get_buttons_conf(models.FemaleCollarButtonsConfiguration, {
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
            dickey=None,
            extra_details=self.extra_details,
            base_layer=self.base_layer
        )
        if self.initials:
            self.add_initials(res, self.initials, self.resolution, self.pocket)

        print("compose", time() - start)
        print("total", time() - total)

        return res


    @classmethod
    def get_initials_configuration(cls, initials, pocket):
        if not initials:
            return

        configurations = models.FemaleInitialsConfiguration.objects.filter(
            font_id=initials['font'], location=initials['location'], pocket=pocket
        ).select_related('font')
        return configurations.first()
