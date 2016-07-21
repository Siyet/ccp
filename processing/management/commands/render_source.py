from django.core.management import BaseCommand

from processing.models.sources import PROJECTION
from processing.rendering.builder import ShirtBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {
            "collar": 34,
            "collar_buttons": 2,
            "cuff": 11,
            "cuff_rounding": 1,
            "hem": 1,
            "placket": 2,
            "pocket": 2,
            "sleeve": 2,
            "custom_buttons_type": 1,
            "custom_buttons": 7,
            'back': 1,
            'dickey': {
                "type": 2,
                "fabric": 433
            },
            'tuck': True
        }

        bldr = ShirtBuilder(data, PROJECTION.front)
        bldr.build_shirt(fabric=576)
