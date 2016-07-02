from django.core.management import BaseCommand
from processing.models import BodySource, Texture
from processing.process import create
from PIL import Image

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('source_id', nargs='+', type=int)

    def handle(self, *args, **options):
        s = BodySource.objects.get(pk=options['source_id'][0])
        src = s.composesource_set.first()

        texture = Texture.objects.get(pk=1)

        sample = {
            "texture": texture.texture.path,
            "uv": [src.cache.get(source_field='uv').file.path],
            "lights": [src.cache.get(source_field='light').file.path],
            "pre_shadows": [src.cache.get(source_field='ao').file.path] if texture.needs_shadow else [],
            "post_shadows": [],
            "tiling": texture.tiling,
            "AA": True
        }
        from time import time
        start = time()
        result = create(**sample)
        print(time() - start)
        result.save('/tmp/result.png')

