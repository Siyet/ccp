from .base import *
import os

INSTALLED_APPS += (
    'debug_toolbar',
)

DEBUG = True

WSGI_APPLICATION = 'core.dev_wsgi.application'

ALLOWED_HOSTS = ['*']