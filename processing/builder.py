from PIL import Image
import numpy as np

from backend.models import Fabric
from dictionaries import models as dictionaries
import models as compose
from process import create


class ShirtBuilder(object):
    def __init__(self, shirt_data, projection):
        self.projection = projection
        self.shirt_data = shirt_data
        self.collar_type = shirt_data.get('collar')  # check
        self.collar_buttons = dictionaries.CollarButtons.objects.get(pk=shirt_data.get('collar_buttons')).buttons
        self.pocket = shirt_data.get('pocket')  # check
        self.cuff = shirt_data.get('cuff')  # check
        self.cuff_rounding = shirt_data.get('cuff_rounding')  # check
        self.custom_buttons_type = shirt_data.get('custom_buttons_type')
        self.custom_buttons = shirt_data.get('custom_buttons')
        self.sleeve = shirt_data.get('sleeve')  # check
        self.hem = shirt_data.get('hem')  # check
        self.placket = shirt_data.get('placket')  # check

    def build_shirt(self, fabric):
        from time import time
        total = time()
        start = time()
        fabric = Fabric.objects.get(pk=fabric)

        texture = fabric.texture

        uv = []
        lights = []
        shadows = []
        post_shadows = []
        alphas = []
        buttons = []
        base_layer = []

        def append_buttons(conf):
            if conf is None:
                return
            # CacheBuilder.create_cache(conf, ('image', 'ao'), compose.ButtonsSourceCache)
            buttons_cache = conf.cache.get(source_field='image')
            ao = conf.cache.filter(source_field='ao').first()
            if conf.projection == compose.PROJECTION.front or not isinstance(conf.content_object,
                                                                             compose.BodyButtonsConfiguration):
                buttons.append({
                    'image': buttons_cache.file.path,
                    'position': buttons_cache.position
                })

                if ao:
                    post_shadows.append({
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
                base_layer.append(buttons_base)

        def append_conf(conf, post_shadow=False):
            if conf is None:
                return
            # CacheBuilder.create_cache(conf, ('uv','ao','light'), compose.ComposeSourceCache)
            uv.append(conf.cache.get(source_field='uv'))
            lights.append(conf.cache.get(source_field='light'))
            if post_shadow:
                cache = conf.cache.get(source_field='ao')
                post_shadows.append({
                    'image': cache.file.path,
                    'position': cache.position
                })
            else:
                shadows.append(conf.cache.get(source_field='ao'))
            alphas.append(conf.cache.get(source_field='uv_alpha'))

        append_conf(self.get_body())
        append_conf(self.get_collar())
        append_conf(self.get_cuff())
        append_conf(self.get_pocket())
        append_conf(self.get_placket(), post_shadow=True)

        if self.projection != compose.PROJECTION.back:
            append_buttons(self.get_buttons())

        append_buttons(self.get_cuff_buttons())
        # append_buttons(self.get_collar_buttons())

        uv = self.compose_uv(*uv)
        light = self.compose_light(lights)
        shadow = self.compose_light(shadows)
        alpha = self.compose_alpha(alphas)

        print("preparation", time() - start)
        start = time()

        res = create(texture.cache.path, uv, light, shadow, post_shadows, alpha, buttons, base_layer)

        print("compose", time() - start)
        print("total", time() - total)

        res.save("/tmp/res.png")

    def get_body(self):
        configuration = compose.BodyConfiguration.objects.get(sleeve_id=self.sleeve, hem_id=self.hem,
                                                              cuff_types__id=self.cuff)
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

    def get_buttons(self):
        buttons_conf = compose.BodyButtonsConfiguration.objects.get(buttons_id=self.custom_buttons_type)
        return buttons_conf.sources.filter(projection=self.projection).first()

    def get_collar_buttons(self):
        collar_buttons_conf = compose.CollarButtonsConfiguration.objects.get(collar_id=self.collar_type,
                                                                             buttons=self.collar_buttons)
        return collar_buttons_conf.sources.filter(projection=self.projection).first()

    def get_cuff_buttons(self):
        cuff_buttons_conf = compose.CuffButtonsConfiguration.objects.get(cuff_id=self.cuff,
                                                                         rounding_types__id=self.cuff_rounding)
        return cuff_buttons_conf.sources.filter(projection=self.projection).first()

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
