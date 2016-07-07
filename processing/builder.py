from PIL import Image

from backend.models import Fabric
from dictionaries import models as dictionaries
import models as compose
from process import create
from cache import CacheBuilder


class ShirtBuilder(object):
    def __init__(self, shirt_data, projection):
        self.projection = projection
        self.shirt_data = shirt_data

    def get_obj(self, shirt_data, model, key):
        return model.objects.get(pk=shirt_data.get(key))

    def prepare(self):
        shirt_data = self.shirt_data
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

    def build_body(self, fabric):
        fabric = Fabric.objects.get(pk=fabric)

        texture = fabric.texture
        configuration = compose.BodySource.objects.get(sleeve_id=self.sleeve, hem_id=self.hem, cuff_types__id=self.cuff)
        compose_model = configuration.sources.get(projection=self.projection)

        collar_conf = compose.CollarSource.objects.get(collar_id=self.collar_type, buttons=self.collar_buttons)
        collar_model = collar_conf.sources.get(projection=self.projection)

        uv = compose_model.cache.get(source_field='uv').file
        light = self.compose_light(compose_model.cache.get(source_field='light'),
                                   collar_model.cache.get(source_field='light'))
        ao = self.compose_light(compose_model.cache.get(source_field='ao'), collar_model.cache.get(source_field='ao'))

        res = create(texture.cache.path, [uv.path], light, ao)

        (collar, collar_pos) = self.compose_part(collar_conf, texture=texture.cache.path)
        res.paste(collar, collar_pos, mask=collar)

        cuff_conf = compose.CuffSource.objects.get(cuff_types__id=self.cuff, rounding_id=self.cuff_rounding)
        (cuff, cuff_pos) = self.compose_part(cuff_conf, texture=texture.cache.path)
        res.paste(cuff, cuff_pos, mask=cuff)

        try:
            pocket_conf = compose.PocketSource.objects.get(pocket_id=self.pocket)
            (pocket, pocket_pos) = self.compose_part(pocket_conf, texture=texture.cache.path)
            res.paste(pocket, pocket_pos, mask=pocket)
        except:
            print("skipping pocket")

        try:
            placket_conf = compose.PlacketSource.objects.get(placket_id=self.placket, hem_id=self.hem)
            (placket, placket_pos) = self.compose_part(placket_conf, texture=texture.cache.path, post_shadow=True)
            placket.save("/tmp/placket.png")
            res.paste(placket, placket_pos, mask=placket)
        except:
            print("skipping placket")

        res.save('/tmp/res.png')

    def compose_part(self, conf, texture, post_shadow=False):
        model = conf.sources.get(projection=self.projection)

        if not model.cache.count():
            CacheBuilder.create_cache(model, ('uv', 'light', 'ao'), compose.ComposeSourceCache)
            model.refresh_from_db()

        ao = model.cache.get(source_field='ao')

        args = [
            texture,
            [model.cache.get(source_field='uv').file.path],
            model.cache.get(source_field='light').file.path,
            ao.file.path if not post_shadow else None
        ]
        kwargs = {
            'post_shadows': [ao.file.path] if post_shadow else [],
            'alpha': model.cache.get(source_field='uv_alpha').file.path
        }

        result = create(*args, **kwargs)
        return (result, ao.position)


    def compose_light(self, *sources):
        base = Image.open(sources[0].file.path)
        for source in sources[1:]:
            source_img = Image.open(source.file.path)
            base.paste(source_img, source.position, mask=source_img)
        return base.convert("RGB")