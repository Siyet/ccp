# coding: utf-8
from __future__ import absolute_import

from import_export import fields

from checkout.import_export.resources.base import BaseResource
from checkout.models import Certificate


class CertificateResource(BaseResource):
    PK_ATTRIBUTE_NAME = 'number'
    PK_COLUMN_NAME = 'Certificate number'

    number = fields.Field(attribute=PK_ATTRIBUTE_NAME, column_name=PK_COLUMN_NAME)
    value = fields.Field(attribute='value', column_name='Value outstanding')

    class Meta:
        model = Certificate
        import_id_fields = ('number', )
        fields = ('number', 'value', )
