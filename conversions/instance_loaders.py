from import_export.instance_loaders import CachedInstanceLoader


class CachedWithPrefetchedInstanceLoader(CachedInstanceLoader):

    def __init__(self, *args, **kwargs):
        self.select_related = kwargs.pop('select_related', [])
        self.prefetch_related = kwargs.pop('prefetch_related', [])
        super(CachedWithPrefetchedInstanceLoader, self).__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super(CachedWithPrefetchedInstanceLoader, self).get_queryset()
        return qs.select_related(*self.select_related).prefetch_related(*self.prefetch_related)

    @staticmethod
    def prepare(select_related=None, prefetch_related=None):
        related = {}
        if select_related:
            related['select_related'] = select_related
        if prefetch_related:
            related['prefetch_related'] = prefetch_related

        @staticmethod
        def create_loader(*args, **kwargs):
            kwargs.update(related)
            return CachedWithPrefetchedInstanceLoader(*args, **kwargs)

        return create_loader


class ForeignPrimaryKeyInstanceLoader(CachedInstanceLoader):
    def __init__(self, *args, **kwargs):
        super(CachedInstanceLoader, self).__init__(*args, **kwargs)

        pk_field_name = self.resource.get_import_id_fields()[0]
        self.pk_field = self.resource.fields[pk_field_name]
        ids = [row[self.pk_field.column_name] for row in self.dataset.dict]

        qs = self.get_queryset().select_related(self.pk_field.attribute)

        # only perform id-based selection when there's not too many objects to fetch.
        # if more than a half of total amount of objects needs to be queried we query all of them
        # to avoid unoptimized sql request
        if len(ids) < qs.count() / 2:
            qs = qs.filter(**{
                "%s__in" % self.pk_field.attribute: ids
            })

        self.all_instances = dict([(self.pk_field.get_value(instance), instance) for instance in qs])
        return

    def get_instance(self, row):
        related_object = self.pk_field.clean(row)
        return self.all_instances.get(related_object) if related_object.id else None
