# coding: utf-8
from __future__ import absolute_import

from itertools import ifilter

from django import forms
from django.contrib import admin
from django.utils.text import ugettext_lazy as _
from import_export.admin import ImportExportMixin
from imagekit.admin import AdminThumbnail

from conversions.resources import FabricResidualResource, FabricResource, TemplateShirtResource
from conversions.mixin import TemplateAndFormatMixin
from backend.widgets import ContentTypeSelect
from grappelli_orderable.admin import GrappelliOrderableAdmin
from .models import *


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
    exclude = ['is_template', 'code', 'showcase_image', 'individualization']


class TemplateShirtAdmin(TemplateAndFormatMixin, ImportExportMixin, GrappelliOrderableAdmin):
    resource_class = TemplateShirtResource
    exclude = ['is_template']
    inlines = [CollarInline, CuffInline, ContrastDetailsInline, ContrastStitchInline, ShirtImageInline]


class StandardShirtAdmin(admin.ModelAdmin):
    exclude = ['is_template', 'code', 'individualization', 'fabric']


class FabricPriceAdmin(admin.ModelAdmin):
    list_display = ['fabric_category', 'storehouse', 'price']
    list_display_links = ['price']

    def get_queryset(self, request):
        queryset = super(FabricPriceAdmin, self).get_queryset(request)
        return queryset.select_related('fabric_category', 'storehouse')


class FabricResidualAdmin(TemplateAndFormatMixin, ImportExportMixin, admin.ModelAdmin):
    resource_class = FabricResidualResource
    list_select_related = ('fabric', 'storehouse',)

    def get_export_queryset(self, request):
        """
        return all data to export
        """
        qs = self.resource_class._meta.model.objects.all()
        if self.list_select_related:
            qs = qs.select_related(*self.list_select_related)
        return qs


class FabricResidualAdminInline(admin.TabularInline):
    model = FabricResidual
    extra = 0


class FabricAdmin(TemplateAndFormatMixin, ImportExportMixin, admin.ModelAdmin):
    RESIDUAL_KEY = "storehouse_%s"
    list_per_page = 20
    resource_class = FabricResource
    search_fields = ('code',)
    list_filter = ('category',)
    readonly_fields = ['category']
    inlines = [FabricResidualAdminInline, ]
    list_select_related = ('category', 'fabric_type', 'thickness', 'texture')

    def __init__(self, *args, **kwargs):
        super(FabricAdmin, self).__init__(*args, **kwargs)
        self.storehouses = Storehouse.objects.all()
        self.bind_storehouse_residuals()

    def bind_storehouse_residuals(self):
        """
        Attaches callable properties to admin class for every fetched storehouse which are resolved to corresponding
        residuals during display cycle
        """
        for storehouse in self.storehouses:
            residual_for_storehouse = lambda self, fabric, storehouse=storehouse: self.get_residual(fabric, storehouse)
            residual_for_storehouse.short_description = storehouse.country
            setattr(FabricAdmin, self.RESIDUAL_KEY % storehouse.id, residual_for_storehouse)

    def get_queryset(self, request):
        queryset = super(FabricAdmin, self).get_queryset(request)
        return queryset.prefetch_related('residuals__storehouse', 'colors', 'designs')

    def get_residual(self, fabric, storehouse):
        residual_predicate = lambda residual: residual.storehouse == storehouse
        residual = next(ifilter(residual_predicate, fabric.residuals.all()), None)
        return residual.amount if residual else None

    def get_list_display(self, request):
        residual_fields = map(lambda storehouse: self.RESIDUAL_KEY % storehouse.id, self.storehouses)
        list_display = ['code', 'category'] + residual_fields + ['material', 'has_description', 'fabric_type',
                                                                 'thickness', 'get_colors', 'get_designs', 'thumbnail']
        return list_display

    def get_list_display_links(self, request, list_display):
        return ('code',)

    # fields
    thumbnail = AdminThumbnail(image_field="get_sample", template='processing/sample.html')
    thumbnail.short_description = _(u'Лоскут')

    def has_description(self, fabric):
        return not (not (fabric.short_description or fabric.long_description))

    has_description.short_description = _(u'Описание')
    has_description.boolean = True

    def get_colors(self, fabric):
        return "; ".join([unicode(color) for color in fabric.colors.all()])

    get_colors.short_description = _(u'Цвета')

    def get_designs(self, fabric):
        return "; ".join([unicode(design) for design in fabric.designs.all()])

    get_designs.short_description = _(u'Дизайн')


class AccessoriesPriceAdminForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(label=_('content type'), queryset=ContentType.objects.all(),
                                          widget=ContentTypeSelect(related_field='id_object_pk'))
    object_pk = forms.ChoiceField(required=False)

    class Meta:
        model = AccessoriesPrice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccessoriesPriceAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['object_pk'].choices = [(None, '')] + [(x.pk, unicode(x)) for x in
                                                               instance.content_type.model_class().objects.all()]
        content_type_pk = [x.pk for x in self.fields['content_type'].queryset if
                           hasattr(x.model_class(), 'get_related_shirts')]
        self.fields['content_type'].queryset = self.fields['content_type'].queryset.filter(pk__in=content_type_pk)
        self.fields['content_type'].choices = [(pk, content_type_names.get(title, title)) for pk, title in
                                               self.fields['content_type'].choices]

    def clean_content_type(self):
        content_type = self.cleaned_data.get('content_type')
        if not hasattr(content_type.model_class(), 'get_related_shirts'):
            raise forms.ValidationError(u'Модель "%s" не связана с ценой рубашки' % content_type)
        if not self.fields['object_pk'].choices:
            self.fields['object_pk'].choices = [(None, '')] + [(x.pk, unicode(x)) for x in
                                                               content_type.model_class().objects.all()]
        return content_type

    def clean_object_pk(self):
        object_pk = self.cleaned_data.get('object_pk')
        if not object_pk:
            return None
        return object_pk


class AccessoriesPriceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_type_title', 'content_object', 'price',)
    list_display_links = ('pk', 'content_type_title', 'content_object', 'price',)
    form = AccessoriesPriceAdminForm


class CollectionAdmin(GrappelliOrderableAdmin):
    list_display = ('title', 'sex')


admin.site.register([
    Storehouse,
    Dickey,
    Initials,
    ElementStitch
])

admin.site.register([Hardness, CustomButtons, ShawlOptions, Stays], GrappelliOrderableAdmin)

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Fabric, FabricAdmin)
admin.site.register(FabricPrice, FabricPriceAdmin)
admin.site.register(FabricResidual, FabricResidualAdmin)
admin.site.register(CustomShirt, CustomShirtAdmin)
admin.site.register(TemplateShirt, TemplateShirtAdmin)
admin.site.register(StandardShirt, StandardShirtAdmin)
admin.site.register(AccessoriesPrice, AccessoriesPriceAdmin)
