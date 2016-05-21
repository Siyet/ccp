# coding: utf-8
from collections import OrderedDict
from copy import deepcopy
import logging
import traceback
from diff_match_patch import diff_match_patch
from django.core.management.color import no_style
from django.db import transaction, connections, DEFAULT_DB_ALIAS
from django.db.transaction import TransactionManagementError, savepoint_commit, atomic
from django.utils import six
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from import_export import resources, fields
from import_export.django_compat import savepoint, savepoint_rollback
from import_export.results import Result, Error, RowResult
import sys
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
import tablib
from backend.models import Fabric, FabricResidual, Storehouse
from dictionaries import models as dictionaries


class CustomForeignKeyWidget(ForeignKeyWidget):

    def clean(self, value):
        val = super(ForeignKeyWidget, self).clean(value)
        if val:
            try:
                return self.model.objects.get(**{self.field: val})
            except self.model.DoesNotExist:
                return self.model(**{self.field: val})
        else:
            return None


class FabricResource(resources.ModelResource):
    code = fields.Field(column_name='Code', attribute='code')
    material = fields.Field(column_name='Fabric', attribute='material')
    colors = fields.Field(column_name='Color', attribute='colors', default=[], widget=ManyToManyWidget(dictionaries.FabricColor, field='title'))
    design = fields.Field(column_name='Design', attribute='designs', default=[], widget=ManyToManyWidget(dictionaries.FabricDesign, field='title'))
    short_description = fields.Field(column_name='Short fabric description', attribute='short_description')
    long_description = fields.Field(column_name='Long fabric description', attribute='long_description')
    fabric_type = fields.Field(column_name='Type', attribute='fabric_type', widget=CustomForeignKeyWidget(dictionaries.FabricType, field='title'))
    thickness = fields.Field(column_name='Thickness', attribute='thickness', widget=CustomForeignKeyWidget(dictionaries.Thickness, field='title'))
    price_category = fields.Field(column_name='Price category', attribute='category', widget=CustomForeignKeyWidget(dictionaries.FabricCategory, field='title'))

    class Meta:
        model = Fabric
        import_id_fields = ('code', )
        fields = ('code', )

    def check_relations(self, instance, field):
        if getattr(instance, field) is not None and getattr(instance, field).pk is None:
            getattr(instance, field).save()
            setattr(instance, field, getattr(instance, field))

    def before_save_instance(self, instance, dry_run):
        if not dry_run:
            self.check_relations(instance, 'category')
            self.check_relations(instance, 'fabric_type')
            self.check_relations(instance, 'thickness')

    @atomic()
    def import_data(self, *args, **kwargs):
        result = super(resources.ModelResource, self).import_data(*args, **kwargs)
        result.rows.sort(key=lambda x: x.new_record, reverse=True)
        return result

    def import_obj(self, obj, data, dry_run):
        for field in self.get_fields():
            if isinstance(field.widget, ManyToManyWidget):
                val = data.get(field.column_name)
                if val is None:
                    val = ''
                setattr(obj, '%s_diff' % field.column_name, val)
                continue
            self.import_field(field, obj, data)

    def get_diff(self, original, current, dry_run=False):
        data = []
        dmp = diff_match_patch()
        for field in self.get_fields():
            v1 = self.export_field(field, original) if original else ""
            v2 = self.export_field(field, current) if current else ""
            if isinstance(field.widget, ManyToManyWidget):
                v2 = getattr(current, '%s_diff' % field.column_name)
            diff = dmp.diff_main(force_text(v1), force_text(v2))
            dmp.diff_cleanupSemantic(diff)
            html = dmp.diff_prettyHtml(diff)
            html = mark_safe(html)
            data.append(html)
        return data


class FabricResidualResource(resources.ModelResource):

    class Meta:
        model = Fabric

    def save_instance(self, instance, dry_run=False):
        self.before_save_instance(instance, dry_run)
        if not dry_run:
            instance.save()
            if instance.residuals_set is not None:
                for country, amount in instance.residuals_set.iteritems():
                    if country == 'Fabric':
                        continue
                    try:
                        amount = float(amount)
                    except (ValueError, TypeError):
                        amount = 0
                    storehouse = next(storehouse for pk, storehouse in self.get_storehouses().iteritems()
                                      if storehouse.country == country)
                    try:
                        residual = next(x for x in instance.residuals.all() if x.storehouse == storehouse)
                    except StopIteration:
                        residual = FabricResidual.objects.create(fabric=instance, storehouse=storehouse)
                    residual.amount = amount
                    residual.save()
        self.after_save_instance(instance, dry_run)

    def get_diff(self, original, current, dry_run=False):
        data = []
        dmp = diff_match_patch()
        v1 = original.code if original else ""
        v2 = current.code if current else ""
        diff = dmp.diff_main(force_text(v1), force_text(v2))
        dmp.diff_cleanupSemantic(diff)
        html = dmp.diff_prettyHtml(diff)
        html = mark_safe(html)
        data.append(html)

        storehouses = self.get_storehouses()
        if original:
            residuals = {x.storehouse_id: x.amount for x in original.residuals.all()}
        else:
            residuals = {}
        for pk, storehouse in storehouses.iteritems():
            v1 = u'%.2f' % residuals.get(pk, 0)
            try:
                v2 = u'%.2f' % float(current.residuals_set.get(storehouse.country, 0))
            except (ValueError, TypeError):
                v2 = u'%.2f' % 0
            diff = dmp.diff_main(force_text(v1), force_text(v2))
            dmp.diff_cleanupSemantic(diff)
            html = dmp.diff_prettyHtml(diff)
            html = mark_safe(html)
            data.append(html)
        return data

    def get_queryset(self):
        return resources.ModelResource.get_queryset(self).prefetch_related('residuals__storehouse')

    def get_storehouses(self, storehouses=None):
        if not hasattr(self, '_storehouses'):
            if storehouses is not None:
                for country in storehouses:
                    Storehouse.objects.get_or_create(country=country)
            storehouses = Storehouse.objects.all()
            self._storehouses = OrderedDict((x.pk, x) for x in storehouses)
        return self._storehouses

    @atomic()
    def import_data(self, dataset, dry_run=False, raise_errors=False,
                    use_transactions=None, **kwargs):
        result = Result()
        storehouses = self.get_storehouses(dataset.headers[1:])
        result.diff_headers = self.get_diff_headers()
        headers = [storehouse.country for pk, storehouse in storehouses.iteritems()]
        headers.insert(0, 'Fabric')
        result.diff_headers = headers

        if use_transactions is None:
            use_transactions = self.get_use_transactions()

        if use_transactions is True:
            real_dry_run = False
            sp1 = savepoint()
        else:
            real_dry_run = dry_run

        try:
            self.before_import(dataset, real_dry_run, **kwargs)
        except Exception as e:
            logging.exception(e)
            tb_info = traceback.format_exc()
            result.base_errors.append(Error(e, tb_info))
            if raise_errors:
                if use_transactions:
                    savepoint_rollback(sp1)
                raise

        fabric_dict = {x.code: x for x in self.get_queryset()}
        numbers = set(map(str, range(10)))
        for row in dataset.dict:
            try:
                row_result = RowResult()
                if not row['Fabric'] or (len(row['Fabric']) > 1 and row['Fabric'][1] not in numbers):
                    continue
                try:
                    instance = fabric_dict[row['Fabric']]
                    new = False
                except KeyError:
                    instance = self._meta.model(code=row['Fabric'])
                    new = True
                instance.residuals_set = row
                if new:
                    row_result.import_type = RowResult.IMPORT_TYPE_NEW
                else:
                    row_result.import_type = RowResult.IMPORT_TYPE_UPDATE
                row_result.new_record = new
                original = deepcopy(instance)
                if self.for_delete(row, instance):
                    if new:
                        row_result.import_type = RowResult.IMPORT_TYPE_SKIP
                        row_result.diff = self.get_diff(None, None, real_dry_run)
                    else:
                        row_result.import_type = RowResult.IMPORT_TYPE_DELETE
                        self.delete_instance(instance, real_dry_run)
                        row_result.diff = self.get_diff(original, None, real_dry_run)
                else:
                    if not real_dry_run:
                        with transaction.atomic():
                            self.save_instance(instance, real_dry_run)
                    row_result.object_repr = force_text(instance)
                    row_result.object_id = instance.pk
                    row_result.diff = self.get_diff(instance, instance, real_dry_run)
            except Exception as e:
                # There is no point logging a transaction error for each row
                # when only the original error is likely to be relevant
                if not isinstance(e, TransactionManagementError):
                    logging.exception(e)
                tb_info = traceback.format_exc()
                row_result.errors.append(Error(e, tb_info, row))
                if raise_errors:
                    if use_transactions:
                        savepoint_rollback(sp1)
                    six.reraise(*sys.exc_info())
            if (row_result.import_type != RowResult.IMPORT_TYPE_SKIP or
                    self._meta.report_skipped):
                result.rows.append(row_result)

        # Reset the SQL sequences when new objects are imported
        # Adapted from django's loaddata
        if not dry_run and any(r.import_type == RowResult.IMPORT_TYPE_NEW for r in result.rows):
            connection = connections[DEFAULT_DB_ALIAS]
            sequence_sql = connection.ops.sequence_reset_sql(no_style(), [self.Meta.model])
            if sequence_sql:
                with connection.cursor() as cursor:
                    for line in sequence_sql:
                        cursor.execute(line)

        if use_transactions:
            if dry_run or result.has_errors():
                savepoint_rollback(sp1)
            else:
                savepoint_commit(sp1)
        result.rows.sort(key=lambda x: x.new_record, reverse=True)
        return result

    def export(self, queryset=None):
        storehouses = self.get_storehouses()
        headers = [storehouse.country for pk, storehouse in storehouses.iteritems()]
        headers.insert(0, 'Fabric')
        data = tablib.Dataset(headers=headers)
        for obj in queryset:
            row = [obj.code]
            residuals = {x.storehouse_id: x.amount for x in obj.residuals.all()}
            for pk in storehouses.iterkeys():
                try:
                    row.append(u'%.2f' % residuals[pk])
                except KeyError:
                    row.append('')
            data.append(row)
        return data
