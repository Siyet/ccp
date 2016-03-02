# coding: utf-8
from django import forms
from django.contrib import admin
from .models import (
    Collection,
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
    ShirtImage
)


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
    exclude = ['is_template', 'code', 'material', 'showcase_image', 'individualization', 'description']

    def get_queryset(self, request):
        return super(CustomShirtAdmin, self).get_queryset(request).filter(is_template=False)


class TemplateShirtAdminForm(forms.ModelForm):

    class Meta:
        model = TemplateShirt
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TemplateShirtAdminForm, self).__init__(*args, **kwargs)
        self.fields['collection'].required = True


class TemplateShirtAdmin(admin.ModelAdmin):
    exclude = ['is_template']
    inlines = [CollarInline, CuffInline, ContrastDetailsInline, ContrastStitchInline, ShirtImageInline]
    form = TemplateShirtAdminForm

    def get_queryset(self, request):
        return super(TemplateShirtAdmin, self).get_queryset(request).filter(is_template=True)


class FabricPriceAdmin(admin.ModelAdmin):
    list_display = ['fabric_category', 'storehouse', 'price']
    list_display_links = ['price']

    def get_queryset(self, request):
        queryset = super(FabricPriceAdmin, self).get_queryset(request)
        return queryset.select_related('fabric_category', 'storehouse')


class FabricAdmin(admin.ModelAdmin):
    readonly_fields = ['category']


class CollectionAdminForm(forms.ModelForm):

    class Meta:
        model = Collection
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CollectionAdminForm, self).__init__(*args, **kwargs)
        self.fields['storehouse'].required = True


class CollectionAdmin(admin.ModelAdmin):
    form = CollectionAdminForm


admin.site.register([
    Storehouse,
    FabricResidual,
    CustomButtons,
    ShawlOptions,
    Dickey,
    Initials,
])

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Fabric, FabricAdmin)
admin.site.register(FabricPrice, FabricPriceAdmin)
admin.site.register(CustomShirt, CustomShirtAdmin)
admin.site.register(TemplateShirt, TemplateShirtAdmin)
