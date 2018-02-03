# coding: utf-8
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from import_export.widgets import ForeignKeyWidget, Widget, ManyToManyWidget

from core.constants import SEX


class ModelCacheMixin(object):
    def _cache_objects(self):
        objects = list(self.model.objects.all())
        self._objects = dict((unicode(getattr(obj, self.field)), obj) for obj in objects)

    def get_object(self, key):
        if not hasattr(self, "_objects"):
            self._cache_objects()

        value_key = unicode(key)
        return self._objects.get(value_key, None)

    def add_object(self, key):
        new_object = self.model(**{self.field: key})
        self._objects[unicode(key)] = new_object
        return new_object


class CustomForeignKeyWidget(ModelCacheMixin, ForeignKeyWidget):
    def clean(self, value):
        if value:
            obj = self.get_object(value)
            if not obj:
                raise ValueError(u"'%s' with '%s' equal to '%s' was not found" % (
                    self.model._meta.verbose_name,
                    self.model._meta.get_field(self.field).verbose_name,
                    value
                ))
            return obj
        else:
            return None


class CachedManyToManyWidget(ModelCacheMixin, ManyToManyWidget):
    def clean(self, value):
        if not value:
            return self.model.objects.none()
        if isinstance(value, float):
            ids = [int(value)]
        else:
            ids = value.split(self.separator)

        objects = map(lambda id: self.get_object(id), ids)
        return filter(None, objects)

    def render(self, value):
        objects = value.all() if hasattr(value, 'all') else value
        ids = [smart_text(getattr(obj, self.field)) for obj in objects]
        return self.separator.join(ids)


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
        _(u'МУЖ'): SEX.male,
        _(u'ЖЕН'): SEX.female
    }

    def get_object(self, key):
        if not hasattr(self, "_objects"):
            self._cache_objects()

        return self._objects.get(key, None)

    def _cache_objects(self):
        objects = list(self.model.objects.all())
        self._objects = {}
        for collection in objects:
            self._objects[(collection.title, collection.sex)] = collection

    def clean(self, value, sex=None):
        val = super(ForeignKeyWidget, self).clean(value)
        sex = self.SEX_DICT.get(sex, None)
        if val:
            return self.get_object((val, sex))

    def render(self, value):
        return unicode(value)
