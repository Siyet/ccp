from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.templatetags.admin_static import static

csrf_protect_m = method_decorator(csrf_protect)


class GrappelliOrderableAdmin(admin.ModelAdmin):
    order_model_field = 'order'
    list_display = ("__str__",)

    class Media:
        js = (static('grappelli_orderable/admin/js/list_reorder.js'),)

    def get_urls(self):
        try:
            from django.conf.urls.defaults import url
        except ImportError:
            from django.conf.urls import url

        patterns = super(GrappelliOrderableAdmin, self).get_urls()
        patterns.insert(
            # insert just before (.+) rule
            # (see django.contrib.admin.options.ModelAdmin.get_urls)
            -1,
            url(
                r'^reorder/$',
                self.reorder_view,
                name=self.get_url_name()
            )
        )
        return patterns

    def get_url_name(self):
        meta = self.model._meta
        model_name = meta.model_name

        return '{0}admin_{1}_{2}_reorder'.format(
            self.admin_site.name, meta.app_label, model_name,
        )

    @csrf_protect_m
    def reorder_view(self, request):
        """The 'reorder' admin view for this model."""
        model = self.model

        if not self.has_change_permission(request):
            raise PermissionDenied

        if request.method == "POST":
            neworder = 1
            for object_id in request.POST.getlist('neworder[]'):
                obj = model.objects.get(pk=object_id)
                setattr(obj, self.order_model_field, neworder)
                obj.save()
                neworder += 1

        return HttpResponse("OK")
