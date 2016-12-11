from modeltranslation.translator import translator, TranslationOptions
from dictionaries import models

class DictionaryTranslation(TranslationOptions):
    fields = ('title',)

translator.register([
    models.SizeOptions,
    models.FabricDesign,
    models.FabricColor,
    models.CollarButtons,
    models.TuckType,
    models.SleeveLength,
    models.CuffRounding,
    models.PocketType,
    models.YokeType,
    models.CuffType,
    models.DickeyType,
    models.HemType,
    models.PlacketType,
    models.CustomButtonsType,
    models.SleeveType,
    models.BackType,
    models.FabricType,
    models.Thickness
], DictionaryTranslation)