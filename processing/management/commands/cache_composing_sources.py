# coding: utf-8

import sys

from django.core.management import BaseCommand

from processing.models import ComposeSource, ButtonsSource, StitchesSource, CuffMask, CollarMask, CuffConfiguration
from processing.cache import CacheBuilder, STITCHES


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.cache_sources(ComposeSource, ['uv', 'light', 'ao'])
        self.cache_sources(ButtonsSource, ['image', 'ao'])
        self.cache_sources(StitchesSource, ['image'], {'image': STITCHES})
        self.cache_sources(CuffMask, ['mask'])
        self.cache_sources(CollarMask, ['mask'])
        self.cache_sources(CuffConfiguration, ['side_mask'])

    def cache_sources(self, model, fields, field_types=None):
        if not field_types:
            field_types = {}
        sys.stdout.write(u'%s\n' % model.__name__)
        count = model.objects.count()
        i = 0
        for src in model.objects.all():
            if src.cache.count() < len(fields):
                try:
                    CacheBuilder.create_cache(src, fields, field_types)
                except Exception as e:
                    print("ERROR: %s" % e.message)
                    print("failed to create cache for %s" % src.object_id)
                    raise
            i += 1
            sys.stdout.write("\rprocessed (%s/%s)" % (i, count))
            sys.stdout.flush()
        sys.stdout.write('\n')
