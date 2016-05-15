# coding: utf-8
from django.db.transaction import atomic
from django.utils.encoding import force_text
from import_export import resources, fields
from import_export.results import RowResult

from checkout.models import Certificate


class CertificateResource(resources.ModelResource):
    number = fields.Field(attribute='number', column_name='Certificate number')
    value = fields.Field(attribute='value', column_name='Value outstanding')

    class Meta:
        model = Certificate
        import_id_fields = ('number', )
        fields = ('number', 'value', )

    @atomic()
    def import_data(self, *args, **kwargs):
        result = super(resources.ModelResource, self).import_data(*args, **kwargs)
        result.rows.sort(key=lambda x: x.new_record, reverse=True)
        if kwargs.get('use_transactions') is True:
            real_dry_run = False
        else:
            real_dry_run = kwargs.get('dry_run', False)
        for cert in Certificate.objects.exclude(number__in=[x['Certificate number'] for x in args[0].dict]):
            row_result = RowResult()
            row_result.new = False
            row_result.import_type = RowResult.IMPORT_TYPE_DELETE
            row_result.diff = self.get_diff(cert, None)
            row_result.object_repr = force_text(cert)
            row_result.object_id = cert.pk
            self.delete_instance(cert, real_dry_run)
            result.rows.insert(0, row_result)
        return result
