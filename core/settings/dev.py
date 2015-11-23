from .base import *
import os

# INSTALLED_APPS += (
#     'debug_toolbar',
# )

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.sqlite3",
        'NAME': os.path.join(BASE_DIR, "costumecode.sql")
    }
}

DEBUG = True

WSGI_APPLICATION = 'core.dev_wsgi.application'

ALLOWED_HOSTS = ['*']