from django.core.management import BaseCommand

from processing.models.sources import PROJECTION
from processing.builder import ShirtBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {
            "collar": 34,
            "collar_buttons": 2,
            "cuff": 3,
            "cuff_rounding": 1,
            "hem": 1,
            "placket": 2,
            "pocket": 2,
            "sleeve": 2,
            "custom_buttons_type": 1,
            "custom_buttons": 7,
        }

        bldr = ShirtBuilder(data, PROJECTION.side)
        bldr.build_shirt(fabric=569)
