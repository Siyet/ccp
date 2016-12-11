# coding: utf-8
import os

LANGUAGES = [
    ('ru', u'Русский'),
    ('en', 'English'),
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'api', 'locale'),
    os.path.join(BASE_DIR, 'core', 'locale'),
    os.path.join(BASE_DIR, 'backend', 'locale'),
    os.path.join(BASE_DIR, 'checkout', 'locale'),
]

LANGUAGE_CODE = 'ru'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_COOKIE_NAME = 'locale'

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_FALLBACK_LANGUAGES = ('ru',)
