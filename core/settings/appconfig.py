# Application settings
from import_export.formats import base_formats

MIN_FABRIC_RESIDUAL = 10

IMPORT_EXPORT_FORMATS = (
    base_formats.CSV,
    base_formats.XLS,
    base_formats.XLSX,
)
