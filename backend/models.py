# coding: UTF-8
__author__ = 'cloud'

from django.db import models
from django.utils.text import ugettext_lazy as _
from colorful.fields import RGBColorField
from model_utils import Choices

HARDNESS = Choices(('very_soft', _(u'Очень мягкий')),
                   ('soft', _(u'Мягкий')),
                   ('hard', _(u'Жесткий')),
                   ('very_hard', _(u'Очень жесткий')),
                   ('no_hardener', _(u'Без уплотнителя')))


class Collection(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    dickey = models.BooleanField(_(u'Манишка'))
    clasp = models.BooleanField(_(u'Застежка под штифты'))
    solid_yoke = models.BooleanField(_(u'Цельная кокетка'))
    shawl = models.BooleanField(_(u'Платок'))


class Storehouse(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    collection = models.ForeignKey(Collection, verbose_name=_(u'Коллекция'))


class FabricColor(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    value = RGBColorField(_(u'Значение'))


class FabricDesign(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)


class FabricPrice(models.Model):
    storehouse = models.ForeignKey(Storehouse, verbose_name=_(u'Склад'), related_name='prices')
    fabric = models.ForeignKey('Fabric', verbose_name=_(u'Ткань'), related_name='prices')
    price = models.DecimalField(_(u'Цена'))


class Fabric(models.Model):
    code = models.CharField(_(u'Артикул'), max_length=10)
    description = models.TextField(_(u'Описание'))
    colors = models.ManyToManyField(FabricColor, verbose_name=_(u'Цвета'), related_name='fabrics')
    designs = models.ManyToManyField(FabricColor, verbose_name=_(u'Дизайн'), related_name='fabrics')
    texture = models.ImageField(_(u'Текстура'))


class FabricResidual(models.Model):
    storehouse = models.ForeignKey(Storehouse, verbose_name=_(u'Склад'), related_name='residuals')
    fabric = models.ForeignKey(Fabric, verbose_name=_(u'Ткань'), related_name='residuals')
    amount = models.DecimalField(_(u'Остаток'))


class CollarButtons(models.Model):
    title = models.CharField(_(u'Название'))


class CollarType(models.Model):
    title = models.CharField(_(u'Название'))
    buttons = models.ManyToManyField(CollarButtons, verbose_name=_(u'Варианты пуговиц'))


class Collar(models.Model):
    STAYS = Choices(('yes', _(u'Да')), ('no', _(u'Нет')), ('removable', _(u'Да, съемные')))
    stays = models.CharField(_(u'Косточки'), choices=STAYS, max_length=10)

    hardness = models.CharField(_(u'Жесткость'), choices=HARDNESS, max_length=15)

    type = models.ForeignKey(CollarType, verbose_name=_(u'Тип'))


class CuffRounding(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)


class CuffType(models.Model):
    title = models.CharField(_(u'Название'), max_length=255)
    rounding = models.ManyToManyField(CuffRounding, verbose_name=_(u'Варианты закругления'))


class Cuff(models.Model):
    hardness = models.CharField(_(u'Жесткость'), choices=HARDNESS, max_length=15)
    sleeve = models.BooleanField(_(u'Рукав'))
    type = models.ForeignKey(CuffType, verbose_name=_(u'Тип'))


class CustomButtons(models.Model):
    # TODO
    pass

class ShirtDetails(models.Model):
    HEM = Choices(('straight', _(u'Прямой')), ('figured', _(u'Фигурный')))
    hem = models.CharField(_(u'Низ'), choices=HEM, max_length=10)

    PLACKET = Choices(('plank', _(u'С планкой')), ('hidden', _(u'Скрытая застежка')), ('no_plank', _(u'Без планки')))
    placket = models.CharField(_(u'Полочка'), choices=PLACKET, max_length=10)

    POCKET = Choices(('none', _(u'Без кармана')), ('rounded', _(u'Закругленные углы')), ('straight', _(u'Прямые углы')))
    pocket = models.CharField(_(u'Карман'), choices=POCKET, max_length=10)

    tuck = models.BooleanField(_(u'Вытачки'))

    BACK = Choices(('no_folds', _(u'Без складок')), ('one_fold', _(u'Одна складка')), ('two_folds', _(u'Две складки')))
    back = models.CharField(_(u'Спинка'), choices=BACK, max_length=10)
