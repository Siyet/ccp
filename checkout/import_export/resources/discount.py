# coding: utf-8
from __future__ import absolute_import

from import_export import fields

from backend.import_export.utils import save_relations
from backend.import_export.widgets import CustomForeignKeyWidget
from checkout.import_export.resources.base import BaseResource
from checkout.models import Discount, Customer


class DiscountResource(BaseResource):
    PK_ATTRIBUTE_NAME = 'customer'
    PK_COLUMN_NAME = 'Client number'

    customer = fields.Field(attribute=PK_ATTRIBUTE_NAME, column_name=PK_COLUMN_NAME,
                            widget=CustomForeignKeyWidget(Customer, field='number'))
    discount_value = fields.Field(attribute='discount_value', column_name='Discount', default=0)

    class Meta:
        model = Discount
        import_id_fields = ('customer', )
        fields = ('customer', 'discount_value', )

    def before_save_instance(self, instance, dry_run):
        if not dry_run:
            save_relations(instance, 'customer')
