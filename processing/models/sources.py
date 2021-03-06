# coding: UTF-8

from django.db import models
from model_utils.choices import Choices
from django.utils.text import ugettext_lazy as _
from imagekit.models import ImageSpecField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from model_utils.models import TimeStampedModel
from .configuration import CachedSource, InitialsConfiguration

from backend.models import ContrastDetails
from processing.upload_path import UploadComposingSource
from processing.specs import TextureSample, TextureSampleThumbnail, Generators
from processing.storage import overwrite_storage
from .configuration import CuffConfiguration
from .mixins import ModelDiffMixin

PROJECTION = Choices(("front", _(u'Передняя')), ("side", _(u"Боковая")), ("back", _(u'Задняя')))

class ProjectionModel(models.Model):
    projection = models.CharField(_(u'Проекция'), max_length=5, choices=PROJECTION)

    class Meta:
        abstract = True


class AbstractComposeSource(CachedSource, ProjectionModel):
    uv = models.FileField(_(u'UV'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/uv/%s'))
    ao = models.FileField(_(u'AO'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/ao/%s'), blank=True)
    light = models.FileField(_(u'Свет'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/light/%s'), blank=True)
    shadow = models.FileField(_(u'Тени'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/shadow/%s'), blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        unique_together = ('content_type', 'object_id', 'projection')
        verbose_name = _(u'Модель сборки')
        verbose_name_plural = _(u'Модели сборки')


class ComposeSource(AbstractComposeSource):
    pass


class ButtonsSource(CachedSource, ProjectionModel):
    image = models.FileField(_(u'Изображение'), storage=overwrite_storage,
                             upload_to=UploadComposingSource("%s/buttons/image/%s"))
    ao = models.FileField(_(u'Тени'), storage=overwrite_storage, upload_to=UploadComposingSource("%s/buttons/ao/%s"),
                          blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id', 'projection')
        verbose_name = _(u'Модель сборки пуговиц')
        verbose_name_plural = _(u'Модели сборки пуговиц')


class CollarMask(CachedSource, ProjectionModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    mask = models.FileField(verbose_name=_(u'Файл маски'), storage=overwrite_storage,
                            upload_to=UploadComposingSource('composesource/%s/%s'))
    element = models.CharField(_(u'Элемент'), choices=ContrastDetails.COLLAR_ELEMENTS, max_length=20)

    class Meta:
        unique_together = ('object_id', 'content_type', 'element', 'projection')
        verbose_name = _(u'Маска воротника')
        verbose_name_plural = _(u'Маски воротника')


class CuffMask(CachedSource, ProjectionModel):
    cuff = models.ForeignKey(CuffConfiguration, related_name='masks')
    mask = models.FileField(verbose_name=_(u'Файл маски'), storage=overwrite_storage,
                            upload_to=UploadComposingSource('composesource/%s/%s'))
    element = models.CharField(_(u'Элемент'), choices=ContrastDetails.CUFF_ELEMENTS, max_length=20)

    class Meta:
        unique_together = ('cuff', 'element', 'projection')
        verbose_name = _(u'Маска манжеты')
        verbose_name_plural = _(u'Маски манжет')


class StitchesSource(CachedSource, ProjectionModel):
    STITCHES_TYPE = Choices(('under', _(u'Под пуговицами')), ('over', _(u'Над пуговицами')))
    type = models.CharField(verbose_name=_(u'Расположение'), choices=STITCHES_TYPE, default=STITCHES_TYPE.under,
                            blank=False, max_length=10)
    image = models.FileField(verbose_name=_(u'Файл ниток'), storage=overwrite_storage,
                             upload_to=UploadComposingSource('stitches/%s/%s'))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id', 'projection', 'type')
        verbose_name = _(u'Модель сборки ниток')
        verbose_name_plural = _(u'Модели сборки ниток')


class Texture(ModelDiffMixin, TimeStampedModel, CachedSource):

    texture = models.ImageField(_(u'Файл текстуры'), storage=overwrite_storage, upload_to='textures')
    needs_shadow = models.BooleanField(_(u'Использовать тени'), default=True)

    gamma_correction = models.BooleanField(_(u'Гамма-коррекция'), default=False)

    sample = ImageSpecField(source='texture', spec=TextureSample, id=Generators.sample)
    sample_thumbnail = ImageSpecField(source='sample', spec=TextureSampleThumbnail, id=Generators.sample_thumbnail)

    class Meta:
        ordering = ('texture',)
        verbose_name = _(u'Текстура')
        verbose_name_plural = _(u'Текстуры')

    def __unicode__(self):
        return self.texture.name


class InitialsPosition(ProjectionModel):
    left = models.FloatField(_(u'Координата X'))
    top = models.FloatField(_(u'Координата Y'))
    rotate = models.IntegerField(_(u'Поворот'), default=0)
    configuration = models.ForeignKey(InitialsConfiguration, related_name='positions')

    class Meta:
        verbose_name = _(u'Позиция инициалов')
        verbose_name_plural = _(u'Позиции инициалов')
