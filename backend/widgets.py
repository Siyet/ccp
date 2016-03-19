from django import forms
from django.core.urlresolvers import reverse


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
