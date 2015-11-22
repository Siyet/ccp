from django.contrib import admin
from .models import ComposingSource

class SourceAdmin(admin.ModelAdmin):
    list_display = ['type', 'file']

admin.site.register(ComposingSource, SourceAdmin)