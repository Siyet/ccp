from django.conf import settings
from django.db import models


class CustomShirtManager(models.Manager):
    def get_queryset(self):
        queryset = super(CustomShirtManager, self).get_queryset().filter(is_template=False, is_standard=False)
        return queryset


class TemplateShirtManager(models.Manager):
    def available(self):
        return self.filter(
            fabric__active=True,
            fabric__residuals__storehouse_id=models.F('collection__storehouse_id'),
            fabric__residuals__amount__gte=settings.MIN_FABRIC_RESIDUAL
        ).select_related('collection').exclude(fabric__texture=None)

    def get_queryset(self):
        queryset = super(TemplateShirtManager, self).get_queryset().filter(is_template=True, is_standard=False)
        return queryset


class StandardShirtManager(models.Manager):
    def get_queryset(self):
        queryset = super(StandardShirtManager, self).get_queryset().filter(is_template=False, is_standard=True)
        return queryset


class FabricManager(models.Manager):
    @property
    def active(self):
        return self.get_queryset().filter(active=True)


class TypedManager(models.Manager):
    def get_queryset(self):
        queryset = super(TypedManager, self).get_queryset().select_related('type')
        return queryset
