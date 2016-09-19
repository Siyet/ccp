# Application settings
from import_export.formats import base_formats

APP_NAME = 'CostumeCode'

MIN_FABRIC_RESIDUAL = 7

IMPORT_EXPORT_FORMATS = (
    base_formats.CSV,
    base_formats.XLS,
    base_formats.XLSX
)

IMAGEKIT_CACHE_BACKEND = 'default'

FABRIC_SAMPLE_SIZE = (512, 512)
FABRIC_SAMPLE_THUMBNAIL_SIZE = (256, 256)

SITE_DOMAIN = 'costumecode.ru'
SITE_INFO_EMAIL = 'contact@costumecode.ru'

ADMIN_ORDER_EMAIL = 'test.cc@wecreateapps.ru'


SHOWCASE_IMAGE_SIZE = (200, 300)
SHOWCASE_DETAILS_IMAGE_SIZE = (540, 720)


# Render

RENDER = {
    'source_size': (4096, 4096),
    'default_size': (2048, 2048),
    'preview_scale': 0.75
}
