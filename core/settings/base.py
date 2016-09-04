# coding: utf-8

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n_sseuc*u7h+p(t(x*zfg2nbu(bslz_dzmoakp8#+&3-q%d2d+'

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli_orderable',
    'smart_selects',
    'imagekit',
    'dictionaries',

    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'crispy_forms',
    'colorful',

    'conversions',
    'import_export',
    'yandex_kassa',
    'wkhtmltopdf',

    'corsheaders',

    'backend',
    'checkout',
    'processing',
    'processing.male_configs',
    'processing.female_configs',

    # should be the last
    'django_cleanup'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware'
)

ROOT_URLCONF = 'core.urls'

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    )
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

RENDER_CACHE_PATH = os.path.join(MEDIA_ROOT, "rendercache")
RENDER_CACHE_URL = os.path.join(MEDIA_URL, 'rendercache')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'costumecode',
    },
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'costumecode-static'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Europe/Moscow'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Database

try:
    from .database import *
except:
    raise Exception("Database specification not found, please create 'database.py' file in 'core/settings' folder")

# Misc

from .appconfig import *
# noinspection PyUnresolvedReferences
from .email import *
try:
    from htmltopdf import *
except:
    print("htmltopdf config not found: PDF creation will fail.")

GRAPPELLI_ADMIN_TITLE = APP_NAME
GRAPPELLI_CLEAN_INPUT_TYPES = False
