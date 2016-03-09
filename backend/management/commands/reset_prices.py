from django.core.management.base import BaseCommand
from django.db import transaction
from backend import models


class Command(BaseCommand):
    help = 'Reset all prices'

    def handle(self, *args, **options):
        with transaction.atomic():
            for shirt in models.Shirt.objects.select_related('collection__storehouse').\
                    prefetch_related('collection__storehouse__prices'):
                shirt.save()
        self.stdout.write('Complete')
