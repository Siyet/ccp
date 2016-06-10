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


class ButtonsComposingSourceInline(admin.TabularInline):
    model = models.ButtonsSource
    fields = ('projection', 'image', 'ao')
    max_num = 3


class ButtonsSourceAdmin(admin.ModelAdmin):
    inlines = [ButtonsComposingSourceInline]

    def get_list_display(self, request):
        return self.get_fields(request)


admin.site.register(models.BodySource, SourceAdmin)
admin.site.register(models.CollarSource, SourceAdmin)
admin.site.register(models.CuffSource, SourceAdmin)
admin.site.register(models.BackSource, SourceAdmin)
admin.site.register(models.PocketSource, SourceAdmin)
admin.site.register(models.PlacketSource, SourceAdmin)
admin.site.register(models.BodyButtonsSource, ButtonsSourceAdmin)
admin.site.register(models.CollarButtonsSource, ButtonsSourceAdmin)
admin.site.register(models.CuffButtonsSource, ButtonsSourceAdmin)
admin.site.register(models.Texture)