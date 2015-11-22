from imagekit import ImageSpec
from graphics import MapIconProcessor
from django.conf import settings

class MapIconSupport(ImageSpec):
    processors = [
        MapIconProcessor(color=settings.ICON_SETTINGS['support']['color'])
    ]
    format = 'PNG'
    autoconvert = True

class MapIconConnection(ImageSpec):
    processors = [
        MapIconProcessor(color=settings.ICON_SETTINGS['connection']['color'])
    ]
    format = 'PNG'
    autoconvert = True

class MapIconSelected(ImageSpec):
    processors = [
        MapIconProcessor(color=settings.ICON_SETTINGS['selected']['color'])
    ]
    format = 'PNG'
    autoconvert = True

class MapIconSupportTransparent(ImageSpec):
    processors = [
        MapIconProcessor(color=settings.ICON_SETTINGS['support']['color'], alpha=settings.ICON_SETTINGS['transparent_alpha'])
    ]
    format = 'PNG'
    autoconvert = True

class MapIconConnectionTransparent(ImageSpec):
    processors = [
        MapIconProcessor(color=settings.ICON_SETTINGS['connection']['color'], alpha=settings.ICON_SETTINGS['transparent_alpha'])
    ]
    format = 'PNG'
    autoconvert = True