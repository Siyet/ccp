from django.contrib import admin
import models


class ComposingSourceInline(admin.TabularInline):
    model = models.ComposeSource
    fields = ('projection', 'uv', 'ao', 'light')
    max_num = 3


class SourceAdmin(admin.ModelAdmin):
    inlines = [ComposingSourceInline]

    def get_list_display(self, request):
        return self.get_fields(request)

admin.site.register(models.BodySource, SourceAdmin)
admin.site.register(models.CollarSource, SourceAdmin)
admin.site.register(models.CuffSource, SourceAdmin)
admin.site.register(models.BackSource, SourceAdmin)
admin.site.register(models.PocketSource, SourceAdmin)
admin.site.register(models.PlacketSource, SourceAdmin)
admin.site.register(models.Texture)