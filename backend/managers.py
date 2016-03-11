from django.conf import settings
from django.db import models

select_amount = {
    'amount': 'SELECT amount FROM backend_fabricresidual WHERE '
              'backend_fabricresidual.storehouse_id = backend_storehouse.id '
              'AND backend_fabricresidual.fabric_id = backend_fabric.id'
}
where_amount = [
    'amount >= %i' % settings.MIN_FABRIC_RESIDUAL
]


class CustomShirtManager(models.Manager):

    def get_queryset(self):
        queryset = models.Manager.get_queryset(self).filter(is_template=False)
        return queryset


class TemplateShirtManager(models.Manager):

    def available(self):
        return self.extra(select=select_amount, where=where_amount)

    def get_queryset(self):
        queryset = models.Manager.get_queryset(self).filter(is_template=True)
        return queryset
