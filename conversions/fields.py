from django.db.models.fields import NOT_PROVIDED
from import_export import fields


class TemplateShirtCollectionField(fields.Field):
    def clean(self, data, sex=None):
        try:
            value = data[self.column_name]
        except KeyError:
            raise KeyError("Column '%s' not found in dataset. Available "
                           "columns are: %s" % (self.column_name,
                                                list(data.keys())))

        try:
            value = self.widget.clean(value, sex)
        except ValueError as e:
            raise ValueError("Column '%s': %s" % (self.column_name, e))

        if not value and self.default != NOT_PROVIDED:
            if callable(self.default):
                return self.default()
            return self.default

        return value

    def save(self, obj, data, sex=None):
        if not self.readonly:
            attrs = self.attribute.split('__')
            for attr in attrs[:-1]:
                obj = getattr(obj, attr, None)
            setattr(obj, attrs[-1], self.clean(data, sex))


class ContrastDetailField(fields.Field):
    def __init__(self, *args, **kwargs):
        self.elements = kwargs.pop('elements')
        super(ContrastDetailField, self).__init__(*args, **kwargs)

    def get_value(self, obj):
        """
        Returns the value of the object's attribute.
        """
        if self.attribute is None:
            return None

        details = [detail for detail in obj.contrast_details.all() if detail.element in self.elements]
        return details
