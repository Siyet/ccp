from django.core.management import BaseCommand

from processing.models.sources import ProjectionModel
from processing.builder import ShirtBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {
            "collar": 8,
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

        bldr = ShirtBuilder(data, ProjectionModel.PROJECTION.front)
        bldr.prepare()
        bldr.build_body(fabric=569)
