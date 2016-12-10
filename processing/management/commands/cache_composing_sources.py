# coding: utf-8

import sys

from django.core.management import BaseCommand

from processing.models import ComposeSource, ButtonsSource, StitchesSource, CuffMask, CollarMask, CuffConfiguration, CACHE_RESOLUTION, Texture
from processing.female_configs.models import FemaleBodySource
from processing.male_configs.models import MaleBodySource
from processing.cache import CacheBuilder, STITCHES


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.cache_sources(ComposeSource, ['uv', 'light', 'ao', 'shadow'])
        self.cache_sources(MaleBodySource, ['uv', 'light', 'ao', 'shadow'])
        self.cache_sources(FemaleBodySource, ['uv', 'light', 'ao', 'shadow'])
        self.cache_sources(ButtonsSource, ['image', 'ao'])
        self.cache_sources(StitchesSource, ['image'], {'image': STITCHES})
        self.cache_sources(CuffMask, ['mask'])
        self.cache_sources(CollarMask, ['mask'])
        self.cache_sources(CuffConfiguration, ['side_mask'])
        self.cache_textures()

    def cache_sources(self, model, fields, field_types=None):
        if not field_types:
            field_types = {}
        sys.stdout.write(u'%s\n' % model.__name__)
        count = model.objects.count()
        i = 0
        for src in model.objects.all():
            if src.cache.count() < len(fields):
                try:
                    # CacheBuilder.create_cache(src, fields, CACHE_RESOLUTION.full, field_types)
                    CacheBuilder.create_cache(src, fields, CACHE_RESOLUTION.preview, field_types)
                except Exception as e:
                    raise
            i += 1
            sys.stdout.write("\rprocessed (%s/%s)" % (i, count))
            sys.stdout.flush()
        sys.stdout.write('\n')

    def cache_textures(self):
        sys.stdout.write('Textures\n')
        count = Texture.objects.count()
        i = 0
        for texture in Texture.objects.all():
            if texture.cache.count() < 2: # preview + full
                try:
                    CacheBuilder.cache_texture(texture)
                except Exception as e:
                    print("failed to create cache for %s" % texture.id)
                    raise
            i += 1
            sys.stdout.write("\rprocessed (%s/%s)" % (i, count))
            sys.stdout.flush()
        sys.stdout.write('\n')
