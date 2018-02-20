# noinspection PyUnresolvedReferences
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['shirts.wecreateapps.ru']

WSGI_APPLICATION = 'core.dev_wsgi.application'

YANDEX_KASSA_DEBUG = False
YANDEX_KASSA_SCID = 21869
YANDEX_KASSA_SHOP_ID = 30291
YANDEX_KASSA_SHOP_PASSWORD = 'XjKMW9ZADM1hFGu25iUf'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/webapps/costumecode/logs/ccback-django.log'
        },
    },
    'loggers': {
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

