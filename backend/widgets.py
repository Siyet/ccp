# coding: utf-8
from django.conf import settings
import os
from django import forms
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from import_export.widgets import Widget
from backend import models


class ContentTypeSelect(forms.Select):

    class Media:
        js = ('backend/contenttype.select.js', )

    def __init__(self, attrs=None, choices=(), related_field=None):
        super(ContentTypeSelect, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)
        self.related_field = related_field

    def render_script(self, id):
        return u'''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#%s').contentTypeSelect();
                        });
                    })('django' in window && django.jQuery ? django.jQuery: jQuery);
                </script>
                ''' % id

    def render(self, name, value, attrs=None, choices=()):
        attrs['data-url'] = reverse('content_type_object_list')
        attrs['data-field'] = self.related_field
        render = forms.Select.render(self, name, value, attrs, choices)
        return render + self.render_script(u'id_%s' % name)


class FabricResidualWidget(Widget):

    def clean(self, value):
        if not value:
            return []
        residuals = []
        for x in value.split(', '):
            country, amount = x.split(': ')
            storehouse = models.Storehouse.objects.get(country=country)
            amount = float(amount)
            residuals.append((storehouse, amount))
        return residuals

    def render(self, value):
        result = [u'%s: %f' % (x.storehouse.country, x.amount) for x in value.all()]
        return u', '.join(result)


class FileWidget(Widget):
    """
    Widget for file fields.
    """

    def clean(self, value):
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, value)):
            raise ValueError(u'Не найден файл %s' % value)
        return value

    def render(self, value):
        return force_text(value)
