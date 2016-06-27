# coding: utf-8
from __future__ import absolute_import

from django.db.transaction import atomic
from django.utils.encoding import force_text
from import_export import resources
from import_export.results import RowResult


class BaseResource(resources.ModelResource):

    @atomic()
    def import_data(self, *args, **kwargs):
        result = super(resources.ModelResource, self).import_data(*args, **kwargs)
        result.rows.sort(key=lambda x: getattr(x, 'new_record', True), reverse=True)
        if kwargs.get('use_transactions') is True:
            real_dry_run = False
        else:
            real_dry_run = kwargs.get('dry_run', False)
        query = {
            '%s__in' % self.PK_ATTRIBUTE_NAME: [x[self.PK_COLUMN_NAME] for x in args[0].dict]
        }
        for obj in self._meta.model.objects.exclude(**query):
            row_result = RowResult()
            row_result.new = False
            row_result.import_type = RowResult.IMPORT_TYPE_DELETE
            row_result.diff = self.get_diff(obj, None)
            row_result.object_repr = force_text(obj)
            row_result.object_id = obj.pk
            self.delete_instance(obj, real_dry_run)
            result.rows.insert(0, row_result)
        return result
