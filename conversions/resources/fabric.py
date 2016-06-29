# coding: utf-8
from __future__ import absolute_import

from django.db.transaction import atomic
from import_export import fields
from import_export import resources

from conversions.utils import save_relations
from conversions.instance_loaders import CachedWithPrefetchedInstanceLoader
from conversions.widgets import CustomForeignKeyWidget, CachedManyToManyWidget
from backend.models import Fabric
from dictionaries import models as dictionaries


class FabricResource(resources.ModelResource):
    code = fields.Field(column_name='Code', attribute='code')
    material = fields.Field(column_name='Fabric', attribute='material')
    colors = fields.Field(column_name='Color', attribute='colors', default=[],
                          widget=CachedManyToManyWidget(dictionaries.FabricColor, field='title'))
    design = fields.Field(column_name='Design', attribute='designs', default=[],
                          widget=CachedManyToManyWidget(dictionaries.FabricDesign, field='title'))
    short_description = fields.Field(column_name='Short fabric description', attribute='short_description')
    long_description = fields.Field(column_name='Long fabric description', attribute='long_description')
    fabric_type = fields.Field(column_name='Type', attribute='fabric_type',
                               widget=CustomForeignKeyWidget(dictionaries.FabricType, field='title'))
    thickness = fields.Field(column_name='Thickness', attribute='thickness',
                             widget=CustomForeignKeyWidget(dictionaries.Thickness, field='title'))
    price_category = fields.Field(column_name='Price category', attribute='category',
                                  widget=CustomForeignKeyWidget(dictionaries.FabricCategory, field='title'))


    class Meta:
        model = Fabric
        import_id_fields = ('code',)
        fields = ('code',)
        skip_unchanged = True
        select_related = ['thickness', 'fabric_type', 'category']
        prefetch_related = ['designs', 'colors']

        @staticmethod
        def instance_loader_class(*args, **kwargs):
            kwargs.update({
                'select_related': FabricResource.Meta.select_related,
                'prefetch_related': FabricResource.Meta.prefetch_related
            })
            return CachedWithPrefetchedInstanceLoader(*args, **kwargs)

    def get_queryset(self):
        qs = super(FabricResource, self).get_queryset()
        return qs.select_related(*self._meta.select_related).prefetch_related(*self._meta.prefetch_related)

    def before_save_instance(self, instance, dry_run):
        if not dry_run:
            save_relations(instance, 'category')
            save_relations(instance, 'fabric_type')
            save_relations(instance, 'thickness')

    @atomic()
    def import_data(self, *args, **kwargs):
        result = super(resources.ModelResource, self).import_data(*args, **kwargs)
        result.rows.sort(key=lambda x: x.new_record, reverse=True)
        return result
