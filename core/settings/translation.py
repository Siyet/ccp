# coding: utf-8

LANGUAGES = [
    ('ru', u'Русский'),
    ('en', 'English'),
]

LANGUAGE_CODE = 'ru'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_COOKIE_NAME = 'locale'

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_FALLBACK_LANGUAGES = ('ru',)
