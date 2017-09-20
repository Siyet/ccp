from django.core.management.base import BaseCommand
from checkout.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.last()

        pdf = order.get_pdf()
        with open("/tmp/order.pdf", "w") as out:
            out.write(pdf)
