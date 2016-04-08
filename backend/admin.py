# coding: utf-8
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.text import ugettext_lazy as _
from import_export.admin import ImportExportMixin
from backend.resources import FabricResource, TemplateShirtResource
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


class TemplateShirtAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = TemplateShirtResource
    formats = settings.IMPORT_EXPORT_FORMATS
    change_list_template = 'admin/backend/change_list_import_export.html'
    import_template_name = 'admin/backend/import.html'
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
    formats = settings.IMPORT_EXPORT_FORMATS


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
