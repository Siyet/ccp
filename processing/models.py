# coding: UTF-8

from django.db import models
from django.contrib.gis.db.models import PolygonField
from model_utils.choices import Choices
from django.utils.text import ugettext_lazy as _
from imagekit.models import ImageSpecField

from dictionaries import models as dictionaries
from upload_path import UploadComposingSource, UploadComposeCache
from .specs import TextureSample, TextureSampleThumbnail, Generators
from backend import models as backend
from .storage import overwrite_storage
from .cache import CacheBuilder


class SourceMixin(object):
    def __unicode__(self):
        return "#%s" % self.id


class BodySource(models.Model, SourceMixin):
    sleeve = models.ForeignKey(dictionaries.SleeveType, verbose_name=_(u'Рукав'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))
    cuff = models.ForeignKey(dictionaries.CuffType, verbose_name=_(u'Манжет'), blank=True, null=True)

    class Meta:
        unique_together = ('sleeve', 'hem', 'cuff')
        verbose_name = _(u'Конфигурация сборки для основы')
        verbose_name_plural = _(u'Конфигурации сборки для основы')


class BackSource(models.Model, SourceMixin):
    back = models.ForeignKey(dictionaries.BackType, verbose_name=_(u'Спинка'))
    tuck = models.BooleanField(verbose_name=_(u'Вытачки'), choices=backend.Shirt.TUCK_OPTIONS, default=False)
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))

    class Meta:
        unique_together = ('back', 'hem', 'tuck')
        verbose_name = _(u'Конфигурация сборки для спинки')
        verbose_name_plural = _(u'Конфигурации сборки для спинки')


class CollarSource(models.Model, SourceMixin):
    collar = models.OneToOneField(dictionaries.CollarType, verbose_name=_(u'Воротник'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для воротника')
        verbose_name_plural = _(u'Конфигурации сборки для воротника')


class CuffSource(models.Model, SourceMixin):
    cuff = models.ForeignKey(dictionaries.CuffType, verbose_name=_(u'Тип манжеты'))
    rounding = models.ForeignKey(dictionaries.CuffRounding, verbose_name=_(u'Тип закругления'), blank=True, null=True)

    class Meta:
        unique_together = ('cuff', 'rounding')
        verbose_name = _(u'Конфигурация сборки для манжет')
        verbose_name_plural = _(u'Конфигурации сборки для манжет')


class PocketSource(models.Model, SourceMixin):
    pocket = models.OneToOneField(dictionaries.PocketType, verbose_name=_(u'Тип кармана'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для кармана')
        verbose_name_plural = _(u'Конфигурации сборки для кармана')


class PlacketSource(models.Model, SourceMixin):
    placket = models.ForeignKey(dictionaries.PlacketType, verbose_name=_(u'Тип полочки'))
    hem = models.ForeignKey(dictionaries.HemType, verbose_name=_(u'Низ'))

    class Meta:
        unique_together = ('placket', 'hem')
        verbose_name = _(u'Конфигурация сборки для полочки')
        verbose_name_plural = _(u'Конфигурации сборки для полочки')


class ProjectionModel(models.Model):
    PROJECTION = Choices(("front", _(u'Передняя')), ("side", _(u"Боковая")), ("back", _(u'Задняя')))
    projection = models.CharField(_(u'Проекция'), max_length=5, choices=PROJECTION)

    class Meta:
        abstract = True


class ComposeSource(ProjectionModel):
    uv = models.FileField(_(u'UV'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/uv/%s'))
    ao = models.FileField(_(u'Тени'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/ao/%s'))
    light = models.FileField(_(u'Свет'), storage=overwrite_storage, upload_to=UploadComposingSource('%s/light/%s'))

    cuff_source = models.ForeignKey(CuffSource, blank=True, null=True)
    back_source = models.ForeignKey(BackSource, blank=True, null=True)
    collar_source = models.ForeignKey(CollarSource, blank=True, null=True)
    body_source = models.ForeignKey(BodySource, blank=True, null=True)
    placket_source = models.ForeignKey(PlacketSource, blank=True, null=True)
    pocket_source = models.ForeignKey(PocketSource, blank=True, null=True)

    class Meta:
        verbose_name = _(u'Модель сборки')
        verbose_name_plural = _(u'Модели сборки')


class SourceCache(models.Model):
    source_field = models.CharField(max_length=10)
    bounding_box = PolygonField()
    file = models.FileField(storage=overwrite_storage, upload_to=UploadComposeCache('composecache/%s/%s'))

    class Meta:
        abstract = True


class ComposeSourceCache(SourceCache):
    source = models.ForeignKey(ComposeSource, related_name='cache')


class BodyButtonsSource(models.Model, SourceMixin):
    buttons = models.OneToOneField(dictionaries.CustomButtonsType, verbose_name=_(u'Пуговицы'))

    class Meta:
        verbose_name = _(u'Конфигурация сборки для основных пуговиц')
        verbose_name_plural = _(u'Конфигурации сборки для основных пуговиц')


class CollarButtonsSource(models.Model, SourceMixin):
    collar = models.ForeignKey(dictionaries.CollarType, verbose_name=_(u'Воротник'))
    buttons = models.ForeignKey(dictionaries.CollarButtons, verbose_name=_(u'Пуговицы'), blank=True, null=True)

    class Meta:
        unique_together = ('collar', 'buttons')
        verbose_name = _(u'Конфигурация сборки для пуговиц воротника')
        verbose_name_plural = _(u'Конфигурации сборки для пуговиц воротника')


class CuffButtonsSource(models.Model, SourceMixin):
    cuff = models.ForeignKey(dictionaries.CuffType, verbose_name=_(u'Манжеты'))
    rounding = models.ForeignKey(dictionaries.CuffRounding, verbose_name=_(u'Тип закругления'), blank=True, null=True)

    class Meta:
        unique_together = ('cuff', 'rounding')
        verbose_name = _(u'Конфигурация сборки для пуговиц манжет')
        verbose_name_plural = _(u'Конфигурации сборки для пуговиц манжет')


class ButtonsSource(ProjectionModel):
    image = models.FileField(_(u'Изображение'), storage=overwrite_storage,
                             upload_to=UploadComposingSource("%s/buttons/image/%s"))
    ao = models.FileField(_(u'Тени'), storage=overwrite_storage, upload_to=UploadComposingSource("%s/buttons/ao/%s"),
                          blank=True, null=True)

    body_buttons = models.ForeignKey(BodyButtonsSource, blank=True, null=True)
    collar_buttons = models.ForeignKey(CollarButtonsSource, blank=True, null=True)
    cuff_buttons = models.ForeignKey(CuffButtonsSource, blank=True, null=True)

    class Meta:
        verbose_name = _(u'Модель сборки пуговиц')
        verbose_name_plural = _(u'Модели сборки пуговиц')


class ButtonsSourceCache(SourceCache):
    source = models.ForeignKey(ButtonsSource)


class Texture(models.Model):
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

    def save(self, *args, **kwargs):
        CacheBuilder.cache_texture(self, save=False)
        super(Texture, self).save(*args, **kwargs)
