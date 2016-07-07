from django.core.management import BaseCommand
from processing.models import ComposeSourceCache, ComposeSource
from processing.cache import CacheBuilder
from processing.process import create

class Command(BaseCommand):
    def handle(self, *args, **options):
        count = ComposeSource.objects.count()
        i = 0
        for src in ComposeSource.objects.all():
            if not src.cache.count():
                CacheBuilder.create_cache(src, ['uv', 'light', 'ao'], ComposeSourceCache)
            i += 1
            print("processed (%s/%s)" % (i, count))

