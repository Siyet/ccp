from django.conf import settings
from django.db import models
from django.db.models.expressions import RawSQL

class CustomShirtManager(models.Manager):

    def get_queryset(self):
        queryset = models.Manager.get_queryset(self).filter(is_template=False)
        return queryset


class TemplateShirtManager(models.Manager):

    def available(self):
        select_amount = RawSQL("""
            SELECT amount
            FROM backend_fabricresidual
            WHERE backend_fabricresidual.storehouse_id = backend_collection.storehouse_id
              AND backend_fabricresidual.fabric_id = backend_shirt.fabric_id
        """, ())

        return self.annotate(amount=select_amount).filter(amount__gte=settings.MIN_FABRIC_RESIDUAL).select_related('collection')

    def get_queryset(self):
        queryset = models.Manager.get_queryset(self).filter(is_template=True)
        return queryset
