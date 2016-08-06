from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.text import ugettext_lazy as _

from backend.forms import RelatedContentTypeForm
from backend.widgets import ContentTypeSelect
from dictionaries.models import DefaultElement


class DefaultElementAdminForm(RelatedContentTypeForm):
    content_type = forms.ModelChoiceField(
        label=_('content type'),
        queryset=ContentType.objects.filter(**DefaultElement.LIMIT_CHOICES),
        widget=ContentTypeSelect(related_field='id_object_pk')
    )

    class Meta:
        model = DefaultElement
        fields = '__all__'
