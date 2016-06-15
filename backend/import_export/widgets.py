# coding: utf-8
from import_export.widgets import ForeignKeyWidget
from backend.models import SEX

class CustomForeignKeyWidget(ForeignKeyWidget):

    def __init__(self, model, field='pk', null=False, *args, **kwargs):
        self.null = null
        super(CustomForeignKeyWidget, self).__init__(model, field, *args, **kwargs)

    def clean(self, value):
        val = super(ForeignKeyWidget, self).clean(value)
        if val:
            try:
                return self.model.objects.get(**{self.field: val})
            except self.model.DoesNotExist:
                return self.model(**{self.field: val})
            except ValueError as e:
                if self.null:
                    return None
                raise e
        else:
            return None


class TemplateShirtCollectionWidget(ForeignKeyWidget):
    SEX_DICT = {
        u'МУЖ': SEX.male,
        u'ЖЕН': SEX.female
    }

    def clean(self, value, sex=None):
        val = super(ForeignKeyWidget, self).clean(value)
        sex = self.SEX_DICT.get(sex, SEX.unisex)
        return self.model.objects.get(**{self.field: val, 'sex': sex}) if val else None
