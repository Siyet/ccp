from .base import *
import os

INSTALLED_APPS += (
    'debug_toolbar',
)

DEBUG = True

WSGI_APPLICATION = 'core.dev_wsgi.application'

ALLOWED_HOSTS = ['*']

YANDEX_KASSA_DEBUG = True
YANDEX_KASSA_SCID = 123
YANDEX_KASSA_SHOP_ID = 123
YANDEX_KASSA_SHOP_PASSWORD = 'password'
