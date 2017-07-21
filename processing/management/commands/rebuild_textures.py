# coding: utf-8

import sys

from django.core.management import BaseCommand

from processing.cache import CacheBuilder
from processing.models import Texture, SourceCache


class Command(BaseCommand):
    def handle(self, *args, **options):
        cached = SourceCache.objects.filter(content_type__model='texture')
        sys.stdout.write('Removing %s textures...\n' % cached.count())
        cached.delete()
        self.cache_textures()

    def cache_textures(self):
        sys.stdout.write('Building textures cache:\n')
        count = Texture.objects.count()
        i = 0
        for texture in Texture.objects.all():
            try:
                CacheBuilder.cache_texture(texture)
            except Exception:
                print("failed to create cache for %s" % texture.id)
                raise
            i += 1
            sys.stdout.write("\rprocessed (%s/%s)" % (i, count))
            sys.stdout.flush()
        sys.stdout.write('\n')
