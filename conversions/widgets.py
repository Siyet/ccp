# coding: utf-8
from import_export.widgets import ForeignKeyWidget, Widget
from backend.models import SEX

class CustomForeignKeyWidget(ForeignKeyWidget):

    def _cache_objects(self):
        objects = list(self.model.objects.all())
        self._objects =  dict((unicode(getattr(obj, self.field)), obj) for obj in objects)

    def clean(self, value, create_missing=False):
        if not hasattr(self, "_objects"):
            self._cache_objects()

        if value:
            value_key = unicode(value)
            try:
                return self._objects[value_key]
            except KeyError:
                new_object = self.model(**{self.field: value})
                self._objects[value_key] = new_object
                return new_object

        else:
            return None


class ChoicesWidget(Widget):
    def __init__(self, choices):
        # cast to dict if needed
        self.choices = choices if isinstance(choices, dict) else dict(choices)

    def clean(self, value):
        # find key by given value
        for key, val in self.choices.iteritems():
            if val == value:
                return key
        return None

    def render(self, value):
        return self.choices.get(value)



class TemplateShirtCollectionWidget(ForeignKeyWidget):
    SEX_DICT = {
        u'МУЖ': SEX.male,
        u'ЖЕН': SEX.female
    }

    def clean(self, value, sex=None):
        val = super(ForeignKeyWidget, self).clean(value)
        sex = self.SEX_DICT.get(sex, SEX.unisex)
        return self.model.objects.get(**{self.field: val, 'sex': sex}) if val else None
