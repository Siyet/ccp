from django.db import models


class CustomShirtManager(models.Manager):

    def get_queryset(self):
        queryset = models.Manager.get_queryset(self).filter(is_template=False)
        return queryset


class TemplateShirtManager(models.Manager):

    def get_queryset(self):
        queryset = models.Manager.get_queryset(self).filter(is_template=True)
        return queryset
