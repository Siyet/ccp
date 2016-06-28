# coding: utf-8
from __future__ import absolute_import

from diff_match_patch import diff_match_patch
from django.db.transaction import atomic
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from import_export import fields
from import_export.widgets import ManyToManyWidget

from import_export import resources
from conversions.utils import save_relations
from conversions.widgets import CustomForeignKeyWidget
from backend.models import Fabric
from dictionaries import models as dictionaries

import itertools


class FabricResource(resources.ModelResource):
    code = fields.Field(column_name='Code', attribute='code')
    material = fields.Field(column_name='Fabric', attribute='material')
    colors = fields.Field(column_name='Color', attribute='colors', default=[],
                          widget=ManyToManyWidget(dictionaries.FabricColor, field='title'))
    design = fields.Field(column_name='Design', attribute='designs', default=[],
                          widget=ManyToManyWidget(dictionaries.FabricDesign, field='title'))
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
        import_id_fields = ('code', )
        fields = ('code', )

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

    # def import_obj(self, obj, data, dry_run):
    #     for field in self.get_fields():
    #         if isinstance(field.widget, ManyToManyWidget):
    #             val = data.get(field.column_name)
    #             if val is None:
    #                 val = ''
    #             setattr(obj, '%s_diff' % field.column_name, val)
    #             continue
    #         self.import_field(field, obj, data)
    #
    # def get_diff(self, original_fields, new, current_fields, dry_run=False):
    #     data = []
    #     dmp = diff_match_patch()
    #     for v1, v2 in itertools.izip(original_fields, current_fields):
    #
    #         if isinstance(field.widget, ManyToManyWidget):
    #             current_value = getattr(current, '%s_diff' % field.column_name)
    #         diff = dmp.diff_main(force_text(v1), force_text(v2))
    #         dmp.diff_cleanupSemantic(diff)
    #         html = dmp.diff_prettyHtml(diff)
    #         html = mark_safe(html)
    #         data.append(html)
    #     return data
