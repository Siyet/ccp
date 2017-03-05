from modeltranslation.translator import translator, TranslationOptions

from checkout.models import Shop


class ShopTranslation(TranslationOptions):
    fields = ('city', 'street', 'extra')


translator.register(Shop, ShopTranslation)
