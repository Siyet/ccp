# coding: utf-8
from __future__ import absolute_import

import sys
import logging
import traceback
from collections import OrderedDict
from copy import deepcopy

import tablib
from diff_match_patch import diff_match_patch
from django.core.management.color import no_style
from django.db import transaction, connections, DEFAULT_DB_ALIAS
from django.db.transaction import TransactionManagementError, savepoint_commit, atomic
from django.utils import six
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from import_export.django_compat import savepoint, savepoint_rollback
from import_export.results import Result, Error, RowResult

from import_export import resources
from backend.models import Fabric, FabricResidual, Storehouse
from core.utils import first
from lazy import lazy


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
                    storehouse = first(lambda s: s.country == country, self.storehouses)
                    residual = first(lambda x: x.storehouse == storehouse, instance.residuals.all())
                    if residual is None:
                        residual = FabricResidual.objects.create(fabric=instance, storehouse=storehouse)
                    residual.amount = amount
                    residual.save()
        self.after_save_instance(instance, dry_run)

    def get_diff(self, original, current, dry_run=False):
        data = []
        dmp = diff_match_patch()
        original_value = original.code if original else ""
        current_value = current.code if current else ""
        diff = dmp.diff_main(force_text(original_value), force_text(current_value))
        dmp.diff_cleanupSemantic(diff)
        html = dmp.diff_prettyHtml(diff)
        html = mark_safe(html)
        data.append(html)

        storehouses = self.storehouses
        if original:
            residuals = {x.storehouse_id: x.amount for x in original.residuals.all()}
        else:
            residuals = {}
        for storehouse in storehouses:
            original_value = u'%.2f' % residuals.get(storehouse.pk, 0)
            try:
                current_value = u'%.2f' % float(current.residuals_set.get(storehouse.country, 0))
            except (ValueError, TypeError):
                current_value = u'%.2f' % 0
            diff = dmp.diff_main(force_text(original_value), force_text(current_value))
            dmp.diff_cleanupSemantic(diff)
            html = dmp.diff_prettyHtml(diff)
            html = mark_safe(html)
            data.append(html)
        return data

    def get_queryset(self):
        return self._meta.model.objects.all().prefetch_related('residuals__storehouse')

    @lazy
    def storehouses(self):
        storehouses = Storehouse.objects.all()
        return list(storehouses)

    @atomic()
    def import_data(self, dataset, dry_run=False, raise_errors=False,
                    use_transactions=None, **kwargs):
        result = Result()
        result.diff_headers = self.get_diff_headers()
        headers = [storehouse.country for storehouse in self.storehouses]
        headers.insert(0, 'Fabric')
        result.diff_headers = headers

        result.totals = OrderedDict([(RowResult.IMPORT_TYPE_NEW, 0),
                                     (RowResult.IMPORT_TYPE_UPDATE, 0),
                                     (RowResult.IMPORT_TYPE_DELETE, 0),
                                     (RowResult.IMPORT_TYPE_SKIP, 0),
                                     (RowResult.IMPORT_TYPE_ERROR, 0),
                                     ('total', len(dataset))])

        result.totals['total'] = len(dataset)

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

        for row in dataset.dict:
            try:
                row_result = RowResult()
                code = row['Fabric']
                if not Fabric.is_valid_code(code):
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
                    result.totals[row_result.import_type] += 1
                    row_result.diff = self.get_diff(instance, instance, real_dry_run)
            except Exception as e:
                # There is no point logging a transaction error for each row
                # when only the original error is likely to be relevant
                if not isinstance(e, TransactionManagementError):
                    logging.exception(e)
                tb_info = traceback.format_exc()
                row_result.errors.append(Error(e, tb_info, row))
                result.totals[row_result.IMPORT_TYPE_ERROR] += 1
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
        queryset = self.get_queryset()
        storehouses = self.storehouses
        headers = [storehouse.country for storehouse in storehouses]
        headers.insert(0, 'Fabric')
        data = tablib.Dataset(headers=headers)
        for obj in queryset:
            row = [obj.code]
            residuals = {x.storehouse_id: x.amount for x in obj.residuals.all()}
            for sh in storehouses:
                try:
                    row.append(u'%.2f' % residuals[sh.pk])
                except KeyError:
                    row.append('')
            data.append(row)
        return data
