from .base import *
import os

INSTALLED_APPS = (
    'debug_toolbar',
) + INSTALLED_APPS

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE_CLASSES

INTERNAL_IPS = ['127.0.0.1']

DEBUG = True

WSGI_APPLICATION = 'core.dev_wsgi.application'

ALLOWED_HOSTS = ['*']

YANDEX_KASSA_DEBUG = True
YANDEX_KASSA_SCID = 123
YANDEX_KASSA_SHOP_ID = 123
YANDEX_KASSA_SHOP_PASSWORD = 'password'
