from django.core.management import BaseCommand
from processing.models import ComposeSourceCache, BodySource, Texture
from processing.cache import CacheBuilder
from processing.process import create

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('source_id', nargs='+', type=int)

    def handle(self, *args, **options):
        s = BodySource.objects.get(pk=options['source_id'][0])
        src = s.composesource_set.first()
        CacheBuilder.create_cache(src, ['uv', 'light', 'ao'], ComposeSourceCache)
