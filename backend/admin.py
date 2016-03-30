# coding: utf-8
from collections import OrderedDict
from copy import deepcopy
import logging
import traceback
from diff_match_patch import diff_match_patch
from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.management.color import no_style
from django.db import transaction, connections, DEFAULT_DB_ALIAS
from django.db.transaction import TransactionManagementError, savepoint_commit, atomic
from django.utils import six
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.text import ugettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.django_compat import savepoint, savepoint_rollback
from import_export.results import Result, Error, RowResult
import sys
import tablib
from backend.widgets import ContentTypeSelect
from .models import (
    Collection,
    Hardness,
    Stays,
    Storehouse,
    Fabric,
    FabricPrice,
    FabricResidual,
    Collar,
    Cuff,
    CustomButtons,
    ShawlOptions,
    Dickey,
    Initials,
    ContrastDetails,
    ContrastStitch,
    CustomShirt, TemplateShirt,
    ShirtImage,
    AccessoriesPrice,
    ElementStitch)


class ShirtImageInline(admin.TabularInline):
    model = ShirtImage
    extra = 1


class CuffInline(admin.StackedInline):
    model = Cuff
    inline_classes = ('grp-open',)


class CollarInline(admin.StackedInline):
    model = Collar
    inline_classes = ('grp-open',)


class ContrastDetailsInline(admin.TabularInline):
    model = ContrastDetails


class ContrastStitchInline(admin.TabularInline):
    model = ContrastStitch


class CustomShirtAdmin(admin.ModelAdmin):
    inlines = [CollarInline, CuffInline, ContrastDetailsInline, ContrastStitchInline]
    exclude = ['is_template', 'code', 'showcase_image', 'individualization', 'description']


class TemplateShirtAdmin(admin.ModelAdmin):
    exclude = ['is_template']
    inlines = [CollarInline, CuffInline, ContrastDetailsInline, ContrastStitchInline, ShirtImageInline]


class FabricPriceAdmin(admin.ModelAdmin):
    list_display = ['fabric_category', 'storehouse', 'price']
    list_display_links = ['price']

    def get_queryset(self, request):
        queryset = super(FabricPriceAdmin, self).get_queryset(request)
        return queryset.select_related('fabric_category', 'storehouse')


class FabricResidualAdminInline(admin.TabularInline):
    model = FabricResidual
    extra = 0


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
                    except ValueError:
                        amount = 0
                    storehouse = next(storehouse for pk, storehouse in self.get_storehouses().iteritems() if storehouse.country == country)
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
            except ValueError:
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
        if storehouses is not None:
            for country in storehouses:
                Storehouse.objects.get_or_create(country=country)
        if not hasattr(self, '_storehouses'):
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
        for row in dataset.dict:
            try:
                row_result = RowResult()
                if not row['Fabric']:
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


class FabricAdmin(ImportExportMixin, admin.ModelAdmin):
    change_list_template = 'admin/backend/change_list_import_export.html'
    import_template_name = 'admin/backend/import.html'
    list_display = ('code', 'category', 'material', )
    list_display_links = ('code', 'category', )
    search_fields = ('code', )
    list_filter = ('category', )
    readonly_fields = ['category']
    resource_class = FabricResource
    inlines = [FabricResidualAdminInline, ]


class AccessoriesPriceAdminForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(label=_('content type'), queryset=ContentType.objects.all(), widget=ContentTypeSelect(related_field='id_object_pk'))
    object_pk = forms.ChoiceField(required=False)

    class Meta:
        model = AccessoriesPrice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccessoriesPriceAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['object_pk'].choices = [(None, '')] + [(x.pk, unicode(x)) for x in instance.content_type.model_class().objects.all()]
        content_type_pk = [x.pk for x in self.fields['content_type'].queryset if hasattr(x.model_class(), 'get_related_shirts')]
        self.fields['content_type'].queryset = self.fields['content_type'].queryset.filter(pk__in=content_type_pk)

    def clean_content_type(self):
        content_type = self.cleaned_data.get('content_type')
        if not hasattr(content_type.model_class(), 'get_related_shirts'):
            raise forms.ValidationError(u'Модель "%s" не связана с ценой рубашки' % content_type)
        if not self.fields['object_pk'].choices:
            self.fields['object_pk'].choices = [(None, '')] + [(x.pk, unicode(x)) for x in content_type.model_class().objects.all()]
        return content_type

    def clean_object_pk(self):
        object_pk = self.cleaned_data.get('object_pk')
        if not object_pk:
            return None
        return object_pk


class AccessoriesPriceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_type', 'content_object', 'price', )
    list_display_links = ('pk', 'content_type', 'content_object', 'price', )
    form = AccessoriesPriceAdminForm


admin.site.register([
    Collection,
    Storehouse,
    FabricResidual,
    CustomButtons,
    ShawlOptions,
    Dickey,
    Initials,
    Hardness,
    Stays,
    ElementStitch,
])

admin.site.register(Fabric, FabricAdmin)
admin.site.register(FabricPrice, FabricPriceAdmin)
admin.site.register(CustomShirt, CustomShirtAdmin)
admin.site.register(TemplateShirt, TemplateShirtAdmin)
admin.site.register(AccessoriesPrice, AccessoriesPriceAdmin)
