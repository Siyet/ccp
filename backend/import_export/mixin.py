from django.conf import settings


class TemplateAndFormatMixin(object):
    formats = settings.IMPORT_EXPORT_FORMATS
    change_list_template = 'admin/backend/change_list_import_export.html'
    import_template_name = 'admin/backend/import.html'
