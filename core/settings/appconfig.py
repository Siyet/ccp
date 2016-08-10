# Application settings
from import_export.formats import base_formats

APP_NAME = 'CostumeCode'

MIN_FABRIC_RESIDUAL = 10

IMPORT_EXPORT_FORMATS = (
    base_formats.CSV,
    base_formats.XLS,
    base_formats.XLSX
)

IMAGEKIT_CACHE_BACKEND = 'default'

FABRIC_SAMPLE_SIZE = (512, 512)
FABRIC_SAMPLE_THUMBNAIL_SIZE = (256, 256)

SITE_DOMAIN = 'costumecode.ru'

ADMIN_ORDER_EMAIL = 'test.cc@wecreateapps.ru'
