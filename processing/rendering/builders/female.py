from django.core.exceptions import ObjectDoesNotExist
from lazy import lazy

from .base import BaseShirtBuilder
from processing.female_configs import models
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
            raise ObjectDoesNotExist("Cuff configuration not found for given parameters: %s" % self.collar)


    @lazy
    def cuff_buttons(self):
        if self.cuff and self.sleeve.cuffs:
            return self.get_buttons_conf(models.FemaleCuffButtonsConfiguration, {
                'cuff_id': self.cuff['type'],
                'rounding_types__id': self.cuff['rounding']
            })

        return None


    def build_shirt(self):
        self._setup()

        body_models = self.get_compose_configurations(models.FemaleBodyConfiguration, {
            'sleeve_id': self.sleeve.id,
            'hem_id': self.hem,
            'cuff_types__id': self.cuff['type'] if self.cuff else None,
            'tuck_id': self.tuck,
        })

        if self.projection == PROJECTION.back:
            if self.sleeve.cuffs:
                self.append_contrasting_part(self.cuff_conf, self.cuff_model, ContrastDetails.CUFF_ELEMENTS)
                self.append_buttons_stitches(self.cuff_buttons)
                cuffs = self.perform_compose()
                self.base_layer.append(cuffs)

            self.append_model(body_models.get(back_id=self.back))
        else:
            self.append_model(body_models.first())
            if self.sleeve.cuffs:
                self.append_contrasting_part(self.cuff_conf, self.cuff_model, ContrastDetails.CUFF_ELEMENTS)
                self.append_buttons_stitches(self.cuff_buttons)

        self.append_contrasting_part(self.collar_conf, self.collar_model, ContrastDetails.COLLAR_ELEMENTS)
        self.append_model(self.get_compose_configuration(models.FemalePocketConfiguration, {
            'pocket_id': self.pocket
        }))
        self.append_model(self.get_compose_configuration(models.FemalePlacketConfiguration, {
            'plackets': self.placket.id,
            'hem_id': self.hem,
            'tuck_id': self.tuck
        }))
        if self.projection == PROJECTION.back and self.yoke:
            self.append_model(self.get_compose_configuration(models.FemaleYokeConfiguration, {
                'yoke_id': self.yoke
            }))

        if self.projection != PROJECTION.back:
            buttons_conf = self.get_buttons_conf(models.FemaleBodyButtonsConfiguration, {
                'plackets': self.placket.id
            })
            self.append_buttons_stitches(buttons_conf)

        self.append_buttons_stitches(self.get_buttons_conf(models.FemaleCollarButtonsConfiguration, {
            'collar_id': self.collar['type'],
            'buttons': self.collar_buttons
        }))

        return self.perform_compose()

    @classmethod
    def get_initials_configuration(cls, initials, pocket):
        if not initials:
            return

        configurations = models.FemaleInitialsConfiguration.objects.filter(
            font_id=initials['font'], location=initials['location'], pocket=pocket
        ).select_related('font')
        return configurations.first()
