# coding: utf-8

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.text import ugettext_lazy as _

from backend.widgets import ContentTypeSelect
from backend.models import AccessoriesPrice


class RelatedContentTypeForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(label=_(u'Тип содержимого'), queryset=ContentType.objects.all(),
                                          widget=ContentTypeSelect(related_field='id_object_pk'))
    object_pk = forms.ChoiceField(label=_(u'Значение'), required=False)

    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RelatedContentTypeForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['object_pk'].choices = \
                [(None, '')] + [(x.pk, unicode(x)) for x in instance.content_type.model_class().objects.all()]

    def clean_object_pk(self):
        object_pk = self.cleaned_data.get('object_pk')
        if not object_pk:
            return None
        return object_pk

    def clean_content_type(self):
        content_type = self.cleaned_data.get('content_type')
        if not self.fields['object_pk'].choices:
            self.fields['object_pk'].choices = \
                [(None, '')] + [(x.pk, unicode(x)) for x in content_type.model_class().objects.all()]
        return content_type


class AccessoriesPriceAdminForm(forms.ModelForm):
    class Meta:
        model = AccessoriesPrice
        fields = '__all__'

    def clean_content_type(self):
        content_type = self.cleaned_data.get('content_type')
        if not hasattr(content_type.model_class(), 'get_shirts'):
            raise forms.ValidationError(u'Модель "%s" не связана с ценой сорочки' % content_type)

        return content_type


class CuffInlineForm(forms.ModelForm):
    def clean_rounding(self):
        cleaned_data = self.cleaned_data
        cuff_type = cleaned_data["type"]
        rounding = cleaned_data["rounding"]

        if not rounding and cuff_type.rounding.count() > 0:
            raise forms.ValidationError(_(u'Пожалуйста, укажите тип закругления'))

        return rounding
