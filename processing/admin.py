from django.contrib import admin
from .models import ComposingSource

class SourceAdmin(admin.ModelAdmin):
    list_display = ['type', 'file']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return ['type']

admin.site.register(ComposingSource, SourceAdmin)