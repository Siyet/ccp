# coding: UTF-8

from django.db import models
from model_utils.choices import Choices
from django.utils.text import ugettext_lazy as _
from imagekit.models import ImageSpecField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from backend.models import ContrastDetails
from processing.upload_path import UploadComposingSource
from processing.specs import TextureSample, TextureSampleThumbnail, Generators
from processing.storage import overwrite_storage
from .configuration import CollarConfiguration, CuffConfiguration

from .mixins import ModelDiffMixin

PROJECTION = Choices(("front", _(u'Передняя')), ("side", _(u"Боковая")), ("back", _(u'Задняя')))

class ProjectionModel(models.Model):
    projection = models.CharField(_(u'Проекция'), max_length=5, choices=PROJECTION)

    class Meta:
        abstract = True


class ComposeSource(ProjectionModel):
    uv = models.FileField(_(u'UV'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/uv/%s'))
    ao = models.FileField(_(u'Тени'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/ao/%s'))
    light = models.FileField(_(u'Свет'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/light/%s'))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id', 'projection')
        verbose_name = _(u'Модель сборки')
        verbose_name_plural = _(u'Модели сборки')


class ButtonsSource(ProjectionModel):
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


class CollarMask(ProjectionModel):
    collar = models.ForeignKey(CollarConfiguration)
    mask = models.FileField(verbose_name=_(u'Файл маски'), storage=overwrite_storage,
                            upload_to=UploadComposingSource('composesource/%s/%s'))
    element = models.CharField(_(u'Элемент'), choices=ContrastDetails.COLLAR_ELEMENTS, max_length=20)

    class Meta:
        unique_together = ('collar', 'element', 'projection')
        verbose_name = _(u'Маска воротника')
        verbose_name_plural = _(u'Маски воротника')


class CuffMask(ProjectionModel):
    cuff = models.ForeignKey(CuffConfiguration)
    mask = models.FileField(verbose_name=_(u'Файл маски'), storage=overwrite_storage,
                            upload_to=UploadComposingSource('composesource/%s/%s'))
    element = models.CharField(_(u'Элемент'), choices=ContrastDetails.CUFF_ELEMENTS, max_length=20)

    class Meta:
        unique_together = ('cuff', 'element', 'projection')
        verbose_name = _(u'Маска манжеты')
        verbose_name_plural = _(u'Маски манжет')


class StitchesSource(ProjectionModel):
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


class Texture(ModelDiffMixin, models.Model):
    TILING = Choices((4, "default", _(u'Стандартный')), (8, "frequent", _(u'Учащенный (х2)')))

    texture = models.ImageField(_(u'Файл текстуры'), storage=overwrite_storage, upload_to='textures')
    tiling = models.PositiveIntegerField(_(u'Тайлинг'), choices=TILING, default=TILING.default)
    needs_shadow = models.BooleanField(_(u'Использовать тени'), default=True)
    sample = ImageSpecField(source='texture', spec=TextureSample, id=Generators.sample)
    sample_thumbnail = ImageSpecField(source='sample', spec=TextureSampleThumbnail, id=Generators.sample_thumbnail)

    cache = models.FileField(storage=overwrite_storage, upload_to='textures/cache', editable=False, null=True)

    class Meta:
        verbose_name = _(u'Текстура')
        verbose_name_plural = _(u'Текстуры')

    def __unicode__(self):
        return self.texture.name

