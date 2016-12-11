from modeltranslation.translator import translator, TranslationOptions

from backend import models


class TitleTranslation(TranslationOptions):
    fields = ('title',)


class CollectionTranslation(TranslationOptions):
    fields = ('title', 'filter_title', 'about_shirt_title', 'text', 'sex', 'tailoring_time')


class FabricTranslation(TranslationOptions):
    fields = ('short_description', 'long_description', 'material')

translator.register([
    models.Hardness,
    models.CustomButtons,
    models.Stays,
    models.ShawlOptions,
    models.ElementStitch,
    models.Fit
], TitleTranslation)
translator.register(models.Collection, CollectionTranslation)
translator.register(models.Fabric, FabricTranslation)
