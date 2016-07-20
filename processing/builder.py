from PIL import Image
import numpy as np

from backend.models import Fabric
from dictionaries import models as dictionaries
import models as compose
from compose import create
from .cache import CacheBuilder
from django.db.models import ObjectDoesNotExist


class ShirtBuilder(object):
    def __init__(self, shirt_data, projection):
        self.projection = projection
        self.shirt_data = shirt_data
        self.collar_type = shirt_data.get('collar')
        self.collar_buttons = dictionaries.CollarButtons.objects.get(pk=shirt_data.get('collar_buttons')).buttons
        self.pocket = shirt_data.get('pocket')
        self.cuff = shirt_data.get('cuff')
        self.cuff_rounding = shirt_data.get('cuff_rounding')
        self.custom_buttons_type = shirt_data.get('custom_buttons_type')
        self.custom_buttons = shirt_data.get('custom_buttons')
        self.sleeve = shirt_data.get('sleeve')
        self.hem = shirt_data.get('hem')
        self.placket = shirt_data.get('placket')
        self.tuck = shirt_data.get('tuck')
        self.back = shirt_data.get('back')
        self.dickey = shirt_data.get('dickey')
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

    def build_shirt(self, fabric):
        from time import time
        total = time()
        start = time()
        fabric = Fabric.objects.get(pk=fabric)

        texture = fabric.texture

        self.append_conf(self.get_compose_configuration(compose.BodyConfiguration, {
            'sleeve_id': self.sleeve,
            'hem_id': self.hem,
            'cuff_types__id': self.cuff
        }))

        self.append_conf(self.get_compose_configuration(compose.DickeyConfiguration, {
            'dickey_id': self.dickey,
            'hem_id': self.hem,
        }))
        self.append_conf(self.get_collar())
        self.append_conf(self.get_cuff())
        self.append_conf(self.get_pocket())
        self.append_conf(self.get_back())
        self.append_conf(self.get_placket(), post_shadow=True)

        if self.projection != compose.PROJECTION.back:
            (buttons, stitches) = self.get_buttons()
            self.append_buttons(buttons)
            self.append_stitches(stitches)

        (buttons, stitches) = self.get_cuff_buttons()
        self.append_buttons(buttons)
        self.append_stitches(stitches)

        (buttons, stitches) = self.get_collar_buttons()
        self.append_buttons(buttons)
        self.append_stitches(stitches)

        uv = self.compose_uv(*self.uv)
        light = self.compose_light(self.lights)
        shadow = self.compose_light(self.shadows)
        alpha = self.compose_alpha(self.alphas)

        print("preparation", time() - start)
        start = time()
        light.save("/tmp/light.png")
        res = create(
            texture=texture.cache.path,
            uv=uv,
            light=light,
            shadow=shadow,
            post_shadows=self.post_shadows,
            alpha=alpha,
            buttons=self.buttons,
            lower_stitches=self.lower_stitches,
            upper_stitches=self.upper_stitches,
            base_layer=self.base_layer
        )

        print("compose", time() - start)
        print("total", time() - total)

        res.save("/tmp/res.png")

    def append_conf(self, conf, post_shadow=False):
        if conf is None:
            return
        CacheBuilder.create_cache(conf, ('uv', 'ao', 'light'), compose.ComposeSourceCache)
        self.uv.append(conf.cache.get(source_field='uv'))
        self.lights.append(conf.cache.get(source_field='light'))
        try:
            shadow = conf.cache.get(source_field='ao')
            if post_shadow:
                self.post_shadows.append({
                    'image': shadow.file.path,
                    'position': shadow.position
                })
            else:
                self.shadows.append(conf.cache.get(source_field='ao'))
        except ObjectDoesNotExist:
            pass
        self.alphas.append(conf.cache.get(source_field='uv_alpha'))

    def append_stitches(self, stitches):
        for conf in stitches:
            try:
                CacheBuilder.create_cache(conf, ['image'], compose.StitchesSourceCache)
            except:
                continue
            cache = conf.cache.get(source_field='image')
            image = {
                'image': cache.file.path,
                'position': cache.position
            }
            if conf.type == compose.StitchesSource.STITCHES_TYPE.under:
                self.lower_stitches.append(image)
            else:
                self.upper_stitches.append(image)

    def append_buttons(self, conf):
        if conf is None:
            return

        try:
            CacheBuilder.create_cache(conf, ('image', 'ao'), compose.ButtonsSourceCache)
        except:
            return
        buttons_cache = conf.cache.get(source_field='image')
        ao = conf.cache.filter(source_field='ao').first()
        if conf.projection == compose.PROJECTION.front or not isinstance(conf.content_object,
                                                                         compose.BodyButtonsConfiguration):
            self.buttons.append({
                'image': buttons_cache.file.path,
                'position': buttons_cache.position
            })

            if ao:
                self.post_shadows.append({
                    'image': ao.file.path,
                    'position': ao.position
                })
        else:
            buttons_base = Image.new("RGBA", (2048, 2048), 0)
            img = Image.open(buttons_cache.file.path)
            buttons_base.paste(img, buttons_cache.position, mask=img)
            if ao:
                shadow = Image.open(ao.file.path)
                buttons_base.paste(shadow, ao.position, mask=shadow)
            self.base_layer.append(buttons_base)

    def get_compose_configuration(self, model, filters):
        configuration = model.objects.get(**filters)
        return configuration.sources.filter(projection=self.projection).first()

    def get_collar(self):
        collar_conf = compose.CollarConfiguration.objects.get(collar_id=self.collar_type, buttons=self.collar_buttons)
        return collar_conf.sources.filter(projection=self.projection).first()

    def get_cuff(self):
        cuff_conf = compose.CuffConfiguration.objects.get(cuff_types__id=self.cuff, rounding_id=self.cuff_rounding)
        return cuff_conf.sources.filter(projection=self.projection).first()

    def get_pocket(self):
        pocket_conf = compose.PocketConfiguration.objects.get(pocket_id=self.pocket)
        return pocket_conf.sources.filter(projection=self.projection).first()

    def get_placket(self):
        placket_conf = compose.PlacketConfiguration.objects.get(placket_id=self.placket, hem_id=self.hem)
        return placket_conf.sources.filter(projection=self.projection).first()

    def get_back(self):
        back_conf = compose.BackConfiguration.objects.get(back_id=self.back, tuck=self.tuck, hem_id=self.hem)
        return back_conf.sources.filter(projection=self.projection).first()

    def get_buttons(self):
        buttons_conf = compose.BodyButtonsConfiguration.objects.get(buttons_id=self.custom_buttons_type)
        return (buttons_conf.sources.filter(projection=self.projection).first(),
                buttons_conf.stitches.filter(projection=self.projection))

    def get_collar_buttons(self):
        collar_buttons_conf = compose.CollarButtonsConfiguration.objects.get(collar_id=self.collar_type,
                                                                             buttons=self.collar_buttons)
        return (collar_buttons_conf.sources.filter(projection=self.projection).first(),
                collar_buttons_conf.stitches.filter(projection=self.projection))

    def get_cuff_buttons(self):
        cuff_buttons_conf = compose.CuffButtonsConfiguration.objects.get(cuff_id=self.cuff,
                                                                         rounding_types__id=self.cuff_rounding)
        return (cuff_buttons_conf.sources.filter(projection=self.projection).first(),
                cuff_buttons_conf.stitches.filter(projection=self.projection))

    def compose_uv(self, *sources):
        base = np.load(sources[0].file.path)
        for source in sources[1:]:
            (x0, y0) = source.position[::-1]
            array = np.load(source.file.path)
            (x1, y1) = array.shape[:2]
            mask = np.logical_or(array[..., 0] > 0, array[..., 1] > 0)
            base[x0: x0 + x1, y0:y0 + y1][mask] = array[mask]
        return base

    def compose_light(self, sources):
        base = Image.open(sources[0].file.path)
        for source in sources[1:]:
            source_img = Image.open(source.file.path)
            base.paste(source_img, source.position, mask=source_img)

        return base.convert("RGB")

    def compose_alpha(self, sources):
        from PIL import ImageChops
        base = Image.open(sources[0].file.path)
        for source in sources[1:]:
            source_img = Image.open(source.file.path)
            layer = Image.new("L", base.size, 0)
            layer.paste(source_img, source.position)
            base = ImageChops.add(base, layer)

        return base
