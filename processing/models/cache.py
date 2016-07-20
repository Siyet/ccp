# coding: UTF-8

from django.db import models

from processing.upload_path import UploadComposeCache
from processing.storage import overwrite_storage

from .sources import ComposeSource, ButtonsSource, StitchesSource
from ast import literal_eval

class SourceCache(models.Model):
    source_field = models.CharField(max_length=10)
    pos_repr = models.CommaSeparatedIntegerField(max_length=20)
    file = models.FileField(storage=overwrite_storage, upload_to=UploadComposeCache('composecache/%s/%s'))

    class Meta:
        abstract = True
        unique_together = ('source', 'source_field')

    @property
    def position(self):
        return tuple(literal_eval(self.pos_repr))

    @position.setter
    def position(self, value):
        ex = lambda: Exception("Invalid value %s for field 'position'; expected tuple of 2 elements" % value)

        try:
            val = tuple(value)
        except:
            raise ex()

        if not len(val) == 2:
            raise ex()

        self.pos_repr = val


class ComposeSourceCache(SourceCache):
    source = models.ForeignKey(ComposeSource, related_name='cache')


class ButtonsSourceCache(SourceCache):
    source = models.ForeignKey(ButtonsSource, related_name='cache')


class StitchesSourceCache(SourceCache):
    source = models.ForeignKey(StitchesSource, related_name='cache')