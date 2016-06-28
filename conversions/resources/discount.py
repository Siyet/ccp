# coding: utf-8
from __future__ import absolute_import

from import_export import fields, resources

from conversions.widgets import CustomForeignKeyWidget
from conversions.utils import save_relations
from conversions.instance_loaders import ForeignPrimaryKeyInstanceLoader
from checkout.models import Discount, Customer

from .base import BatchReplaceableResource


class DiscountResource(BatchReplaceableResource):
    PK_ATTRIBUTE_NAME = 'customer'
    PK_COLUMN_NAME = 'Client number'

    customer = fields.Field(attribute=PK_ATTRIBUTE_NAME, column_name=PK_COLUMN_NAME,
                            widget=CustomForeignKeyWidget(Customer, field='number'))
    discount_value = fields.Field(attribute='discount_value', column_name='Discount', default=0)

    class Meta:
        model = Discount
        import_id_fields = ('customer',)
        fields = ('customer', 'discount_value',)
        instance_loader_class = ForeignPrimaryKeyInstanceLoader
        skip_unchanged = True

    def before_save_instance(self, instance, dry_run):
        if not dry_run:
            save_relations(instance, 'customer')
