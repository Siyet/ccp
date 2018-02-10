# coding: utf-8
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.text import ugettext_lazy as _
from colorful.fields import RGBColorField
from django.db.models import Count
from model_utils import Choices

from ordered_model.models import OrderedModel


class ComponentModel(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    picture = models.ImageField(_(u'Изображение'), upload_to='component')

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        abstract = True


class Color(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255, default=u'')
    color = RGBColorField(_(u'Значение'))

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Цвет (для инициалов)')
        verbose_name_plural = _(u'Цвета (для инициалов)')


class Font(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    font = models.FileField(_(u'Файл шрифта'), upload_to='fonts')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Шрифт (для инициалов)')
        verbose_name_plural = _(u'Шрифты (для инициалов)')


class FabricColor(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    value = RGBColorField(_(u'Значение'))
    image = models.ImageField(_(u'Изображение'), upload_to='fabriccolor', blank=True)

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Цвет ткани')
        verbose_name_plural = _(u'Цвета тканей')

    @staticmethod
    def used():
        return FabricColor.objects.prefetch_related('color_fabrics').annotate(
            fabrics_count=Count('color_fabrics')).filter(fabrics_count__gt=0)


class FabricCategory(models.Model):
    title = models.CharField(_(u'Категория'), unique=True, max_length=1, db_index=True)

    def __unicode__(self):
        return u"%s %s" % (_(u'Категория'), self.title)

    class Meta:
        verbose_name = _(u'Категория ткани')
        verbose_name_plural = _(u'Категории тканей')


class FabricType(OrderedModel):
    title = models.CharField(_(u'Тип'), unique=True, max_length=255)

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Тип ткани')
        verbose_name_plural = _(u'Типы тканей')


class FabricDesign(ComponentModel):
    class Meta(ComponentModel.Meta):
        verbose_name = _(u'Паттерн ткани')
        verbose_name_plural = _(u'Паттерны тканей')

    @staticmethod
    def used():
        return FabricDesign.objects.prefetch_related('design_fabrics').annotate(
            fabrics_count=Count('design_fabrics')).filter(fabrics_count__gt=0)


class CollarType(ComponentModel):
    buttons = models.ManyToManyField('CollarButtons', verbose_name=_(u'Варианты пуговиц'))

    class Meta(ComponentModel.Meta):
        verbose_name = _(u'Тип воротника')
        verbose_name_plural = _(u'Типы воротников')


class CollarButtons(OrderedModel):
    BUTTONS_CHOICES = Choices(0, 1, 2)

    title = models.CharField(_(u'Название'), max_length=255)
    types = models.ManyToManyField('CollarType', verbose_name=_(u'Типы воротников'), through=CollarType.buttons.through,
                                   blank=True)
    buttons = models.IntegerField(_(u'Количество пуговиц'), choices=BUTTONS_CHOICES, default=1)

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Пуговицы воротника')
        verbose_name_plural = _(u'Пуговицы воротника')


class CuffType(ComponentModel):
    rounding = models.ManyToManyField('CuffRounding', verbose_name=_(u'Варианты закругления'), blank=True)

    class Meta(ComponentModel.Meta):
        verbose_name = _(u'Тип манжеты')
        verbose_name_plural = _(u'Типы манжет')


class CuffRounding(models.Model):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)
    types = models.ManyToManyField('CuffType', verbose_name=_(u'Типы'), through=CuffType.rounding.through, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Тип закругления манжеты')
        verbose_name_plural = _(u'Типы закругления манжеты')


class CustomButtonsType(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    extra_price = models.DecimalField(_(u'Добавочная стоимость'), decimal_places=2, max_digits=10)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Тип пуговиц')
        verbose_name_plural = _(u'Типы пуговиц')

    def get_shirts(self):
        return self.back_shirts.filter(custom_buttons__isnull=False).values_list('id', flat=True).distinct()


class YokeType(ComponentModel):
    class Meta(ComponentModel.Meta):
        verbose_name = _(u'Тип кокетки')
        verbose_name_plural = _(u'Типы кокетки')


class StitchColor(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255)
    color = RGBColorField(_(u'Цвет'))

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Цвет отстрочки')
        verbose_name_plural = _(u'Цвета отстрочки')


class DickeyType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип манишки')
        verbose_name_plural = _(u'Типы манишки')


class SizeOptions(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255)
    show_sizes = models.BooleanField(_(u'Показывать размеры'), default=True)

    def __unicode__(self):
        return self.title

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Вариант размера')
        verbose_name_plural = _(u'Варианты размеров')


class Size(OrderedModel):
    size = models.PositiveIntegerField(_(u'Размер'), unique=True, primary_key=True)

    def __unicode__(self):
        return "%s" % self.size

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Размер сорочки')
        verbose_name_plural = _(u'Размеры сорочек')


class HemType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип низа')
        verbose_name_plural = _(u'Типы низа')


class SleeveType(ComponentModel):
    cuffs = models.BooleanField(_(u'Манжеты'), default=True)

    class Meta:
        verbose_name = _(u'Тип рукава')
        verbose_name_plural = _(u'Типы рукавов')


class PlacketType(ComponentModel):
    show_buttons = models.BooleanField(_(u'Пуговицы видны'), default=True)

    class Meta:
        verbose_name = _(u'Тип полочки')
        verbose_name_plural = _(u'Типы полочек')


class PocketType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип кармана')
        verbose_name_plural = _(u'Типы карманов')


class BackType(ComponentModel):
    class Meta:
        verbose_name = _(u'Тип спинки')
        verbose_name_plural = _(u'Типы спинок')


class TuckType(ComponentModel):
    class Meta(ComponentModel.Meta):
        verbose_name = _(u'Тип вытачек')
        verbose_name_plural = _(u'Типы вытачек')


class Thickness(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Толщина ткани')
        verbose_name_plural = _(u'Толщина ткани')

    def __unicode__(self):
        return self.title


class SleeveLength(OrderedModel):
    title = models.CharField(_(u'Название'), max_length=255, unique=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _(u'Тип длины рукава')
        verbose_name_plural = _(u'Типы длины рукава')

    def __unicode__(self):
        return self.title


class DefaultElement(models.Model):
    LIMIT_CHOICES = {'model__in': ['shawloptions', 'sleevetype']}

    content_type = models.OneToOneField(ContentType, verbose_name=_(u'Тип элемента'), limit_choices_to=LIMIT_CHOICES)
    object_pk = models.PositiveIntegerField(_(u'Элемент по умолчанию'))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta:
        verbose_name = _(u'Элемент по умолчанию')
        verbose_name_plural = _(u'Элементы по умолчанию')

    def __unicode__(self):
        return u'%s: %s' % (self.content_type, self.content_object)


@deconstructible
class ResolveDefault(object):
    def __init__(self, model):
        self.model = model

    def __call__(self):
        model_ct = ContentType.objects.get_for_model(self.model)
        try:
            default = DefaultElement.objects.get(content_type=model_ct)
            return default.object_pk
        except DefaultElement.DoesNotExist:
            return None


def resolve_default_object(model):
    model_ct = ContentType.objects.get_for_model(model)
    try:
        default = DefaultElement.objects.get(content_type=model_ct)
        return model.objects.get(pk=default.object_pk)
    except DefaultElement.DoesNotExist:
        return None

