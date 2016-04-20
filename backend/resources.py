# coding: utf-8
from collections import OrderedDict
from copy import deepcopy
import logging
import traceback
from diff_match_patch import diff_match_patch
from django.core.management.color import no_style
from django.db import transaction, connections, DEFAULT_DB_ALIAS
from django.db.models.fields import NOT_PROVIDED
from django.db.transaction import TransactionManagementError, savepoint_commit, atomic
from django.utils import six
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from import_export import resources, fields
from import_export.django_compat import savepoint, savepoint_rollback
from import_export.results import Result, Error, RowResult
import sys
from import_export.widgets import ForeignKeyWidget
import tablib
from backend.models import Fabric, FabricResidual, Storehouse, TemplateShirt, Collection
from dictionaries import models as dictionaries


class CustomForeignKeyWidget(ForeignKeyWidget):

    def __init__(self, model, field='pk', null=False, *args, **kwargs):
        self.null = null
        super(CustomForeignKeyWidget, self).__init__(model, field, *args, **kwargs)

    def clean(self, value):
        val = super(ForeignKeyWidget, self).clean(value)
        if val:
            try:
                return self.model.objects.get(**{self.field: val})
            except self.model.DoesNotExist:
                return self.model(**{self.field: val})
            except ValueError as e:
                if self.null:
                    return None
                raise e

        else:
            return None


class TemplateShirtCollectionWidget(ForeignKeyWidget):

    def clean(self, value, sex=None):
        val = super(ForeignKeyWidget, self).clean(value)
        if sex == u'МУЖ':
            sex = 'male'
        elif sex == u'ЖЕН':
            sex = 'female'
        else:
            sex = 'unisex'
        return self.model.objects.get(**{self.field: val, 'sex': sex}) if val else None


class TemplateShirtCollectionField(fields.Field):

    def clean(self, data, sex=None):
        try:
            value = data[self.column_name]
        except KeyError:
            raise KeyError("Column '%s' not found in dataset. Available "
                           "columns are: %s" % (self.column_name,
                                                list(data.keys())))

        try:
            value = self.widget.clean(value, sex)
        except ValueError as e:
            raise ValueError("Column '%s': %s" % (self.column_name, e))

        if not value and self.default != NOT_PROVIDED:
            if callable(self.default):
                return self.default()
            return self.default

        return value

    def save(self, obj, data, sex=None):
        if not self.readonly:
            attrs = self.attribute.split('__')
            for attr in attrs[:-1]:
                obj = getattr(obj, attr, None)
            setattr(obj, attrs[-1], self.clean(data, sex))


class TemplateShirtResource(resources.ModelResource):
    code = fields.Field(attribute='code', column_name='Shirt Code')
    fabric = fields.Field(attribute='fabric', column_name=u'Код ткани', widget=CustomForeignKeyWidget(Fabric, field='code'))
    size_option = fields.Field(attribute='size_option', column_name=u'Размер', widget=CustomForeignKeyWidget(model=dictionaries.SizeOptions, field='title'))
    size = fields.Field(attribute='size', column_name=u'№ размера', widget=CustomForeignKeyWidget(model=dictionaries.Size, field='size'))
    hem = fields.Field(attribute='hem', column_name=u'Низ', widget=CustomForeignKeyWidget(model=dictionaries.HemType, field='title'))
    placket = fields.Field(attribute='placket', column_name=u'Полочка', widget=CustomForeignKeyWidget(model=dictionaries.PlacketType, field='title'))
    back = fields.Field(attribute='back', column_name=u'Спинка', widget=CustomForeignKeyWidget(model=dictionaries.BackType, field='title'))
    pocket = fields.Field(attribute='pocket', column_name=u'Карман', widget=CustomForeignKeyWidget(model=dictionaries.PocketType, field='title'))
    collection = TemplateShirtCollectionField(attribute='collection', column_name=u'Коллекция',
                                              widget=TemplateShirtCollectionWidget(Collection, field='title'))

    class Meta:
        model = TemplateShirt
        import_id_fields = ('code', )
        fields = ('code', )

    def before_save_instance(self, instance, dry_run):
        if not dry_run:
            def check_relations(instance, field):
                if getattr(instance, field) is not None and getattr(instance, field).pk is None:
                    getattr(instance, field).save()
                    setattr(instance, field, getattr(instance, field))

            check_relations(instance, 'fabric')
            check_relations(instance, 'collection')
            check_relations(instance, 'hem')
            check_relations(instance, 'placket')
            check_relations(instance, 'size_option')
            check_relations(instance, 'pocket')
            check_relations(instance, 'back')

            if instance.size is not None and instance.size._state.adding:
                instance.size.save()
                instance.size = instance.size

    def import_field(self, field, obj, data):
        if field.attribute and field.column_name in data:
            if field.attribute == 'collection':
                field.save(obj, data, sex=data.get(u'Пол'))
            else:
                field.save(obj, data)


class FabricResource(resources.ModelResource):

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
