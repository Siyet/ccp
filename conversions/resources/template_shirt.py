# coding: utf-8
from __future__ import absolute_import

import tablib
from import_export import fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export import resources

from conversions.fields import TemplateShirtCollectionField
from conversions.utils import save_relations
from conversions.instance_loaders import CachedWithPrefetchedInstanceLoader
from conversions.widgets import CustomForeignKeyWidget, TemplateShirtCollectionWidget, ChoicesWidget
from backend.models import Fabric, TemplateShirt, Collection, Collar, Hardness, Stays, Cuff, CustomButtons, Dickey, \
    Initials, ContrastStitch, ElementStitch, ContrastDetails
from dictionaries import models as dictionaries


class TemplateShirtResource(resources.ModelResource):
    BUTTONS_DEFAULT_DICT = {
        True: u'Пожалуйста, используйте стандартные пуговицы',
        False: u''
    }
    CONTRAST_STITCHES_USE_DICT = {
        True: u'Я хочу использовать отстрочку контрастного цвета',
        False: u'Я не хочу использовать отстрочку контрастного цвета'
    }
    CLASP_USE_DICT = {
        True: u'Я хочу использовать застежку под штифты',
        False: u'Я не хочу использовать застежку под штифты',
    }
    DICKEY_USE_DICT = {
        True: u'Я хочу использовать манишку',
        False: u'Я не хочу использовать манишку',
    }
    SHIRT_CONTRAST_DETAILS_USE_DICT = {
        True: u'Я хочу использовать контрастные ткани',
        False: u'Я не хочу использовать контрастные ткани',
    }
    INITIALS_USE_DICT = {
        True: u'Я хочу использовать инициалы',
        False: u'Я не хочу использовать инициалы'
    }

    TUCK_NOT_USE_CONSTANT = u'Без вытачки'

    COLLECTION_ATTRIBUTE_MAP = {'collection'}
    TUCK_ATTRIBUTE_MAP = {'tuck'}
    CLASP_ATTRIBUTE_MAP = {'clasp'}
    CUFF_ATTRIBUTE_LIST = ('shirt_cuff__type', 'shirt_cuff__rounding', 'shirt_cuff__hardness')
    DICKEY_ATTRIBUTE_MAP = {'dickey__type', 'dickey__fabric'}
    INITIALS_ATTRIBUTE_MAP = {'initials__font', 'initials__color', 'initials__location'}
    INITIALS_CHOICES_ATTRIBUTE_MAP = {'initials__location'}

    SEX_COLUMN_NAME = u'Пол'
    TUCK_COLUMN_NAME = u'Вытачки'
    CLASP_COLUMN_NAME = u'Застежка под штифты'
    DICKEY_COLUMN_NAME = u'Манишка'
    CUFF_COLUMN_NAME = u'Манжеты'
    INITIALS_COLUMN_NAME = u'Инициалы'

    code = fields.Field(attribute='code', column_name='Shirt Code')
    fabric = fields.Field(attribute='fabric', column_name=u'Код ткани',
                          widget=CustomForeignKeyWidget(Fabric, field='code'))
    size_option = fields.Field(attribute='size_option', column_name=u'Размер',
                               widget=CustomForeignKeyWidget(model=dictionaries.SizeOptions, field='title'))
    size = fields.Field(attribute='size', column_name=u'№ размера',
                        widget=CustomForeignKeyWidget(model=dictionaries.Size, field='size'))
    hem = fields.Field(attribute='hem', column_name=u'Низ',
                       widget=CustomForeignKeyWidget(model=dictionaries.HemType, field='title'))
    placket = fields.Field(attribute='placket', column_name=u'Полочка',
                           widget=CustomForeignKeyWidget(model=dictionaries.PlacketType, field='title'))
    pocket = fields.Field(attribute='pocket', column_name=u'Карман',
                          widget=CustomForeignKeyWidget(model=dictionaries.PocketType, field='title'))
    tuck = fields.Field(attribute='tuck', column_name=TUCK_COLUMN_NAME,
                        widget=ChoicesWidget(choices=TemplateShirt.TUCK_OPTIONS))
    back = fields.Field(attribute='back', column_name=u'Спинка',
                        widget=CustomForeignKeyWidget(model=dictionaries.BackType, field='title'))
    collection = TemplateShirtCollectionField(attribute='collection', column_name=u'Коллекция',
                                              widget=TemplateShirtCollectionWidget(Collection, field='title'))
    stitch = fields.Field(attribute='stitch', column_name=u'Отстрочка (мм)',
                          widget=ChoicesWidget(choices=TemplateShirt.STITCH))
    yoke = fields.Field(attribute='yoke', column_name=u'Цельная кокетка',
                        widget=CustomForeignKeyWidget(dictionaries.YokeType, field='title'))
    clasp = fields.Field(attribute='clasp', column_name=CLASP_COLUMN_NAME, widget=ChoicesWidget(choices=CLASP_USE_DICT))
    sleeve = fields.Field(attribute='sleeve', column_name=u'Рукав',
                                      widget=CustomForeignKeyWidget(model=dictionaries.SleeveType, field='title'))
    # Импорт воротника
    collar__type = fields.Field(attribute='collar__type', column_name=u'Тип воротника',
                                widget=CustomForeignKeyWidget(model=dictionaries.CollarType, field='title'))
    collar__hardness = fields.Field(attribute='collar__hardness', column_name=u'Жесткость воротника',
                                    widget=CustomForeignKeyWidget(model=Hardness, field='title'))
    collar__stays = fields.Field(attribute='collar__stays', column_name=u'Косточки',
                                 widget=CustomForeignKeyWidget(model=Stays, field='title'))
    collar__size = fields.Field(attribute='collar__size', column_name=u'Размер воротника',
                                widget=CustomForeignKeyWidget(model=dictionaries.CollarButtons, field='title'))

    # Импорт манжеты
    shirt_cuff__type = fields.Field(attribute='shirt_cuff__type', column_name=CUFF_COLUMN_NAME,
                                    widget=CustomForeignKeyWidget(model=dictionaries.CuffType, field='title'))
    shirt_cuff__rounding = fields.Field(attribute='shirt_cuff__rounding', column_name=u'Вид манжеты',
                                        widget=CustomForeignKeyWidget(model=dictionaries.CuffRounding, field='title'))
    shirt_cuff__hardness = fields.Field(attribute='shirt_cuff__hardness', column_name=u'Жесткость манжеты',
                                        widget=CustomForeignKeyWidget(model=Hardness, field='title'))
    # Импорт пуговиц
    custom_buttons_type = fields.Field(attribute='custom_buttons_type', column_name=u'Пуговицы',
                                       widget=CustomForeignKeyWidget(model=dictionaries.CustomButtonsType,
                                                                     field='title',
                                                                     create_missing=False))
    custom_buttons = fields.Field(attribute='custom_buttons', column_name=u'Код цвета пуговицы',
                                  widget=CustomForeignKeyWidget(model=CustomButtons, field='title',
                                                                create_missing=False))
    # импорт манишки
    dickey__type = fields.Field(attribute='dickey__type', column_name=u'МА Тип',
                                widget=CustomForeignKeyWidget(dictionaries.DickeyType, field='title',
                                                              create_missing=False))
    dickey__fabric = fields.Field(attribute='dickey__fabric', column_name=u'МА Ткань',
                                  widget=CustomForeignKeyWidget(Fabric, field='code', create_missing=False))
    # импорт инициалов
    initials__font = fields.Field(attribute='initials__font', column_name=u'ИН Шрифт',
                                  widget=ForeignKeyWidget(dictionaries.Font, field='title'))
    initials__color = fields.Field(attribute='initials__color', column_name=u'ИН Цвет',
                                   widget=ForeignKeyWidget(dictionaries.Color, field='title'))
    initials__location = fields.Field(attribute='initials__location', column_name=u'ИН Позиция')
    # контрастные отстрочки
    contrast_stitch_shirt = fields.Field(attribute='contrast_stitch_shirt', column_name=u'ОТЦ Сорочка')
    contrast_stitch_cuff = fields.Field(attribute='contrast_stitch_cuff', column_name=u'ОТЦ Манжеты')
    contrast_stitch_collar = fields.Field(attribute='contrast_stitch_collar', column_name=u'ОТЦ Воротник')
    contrast_stitch_loops = fields.Field(attribute='contrast_stitch_loops', column_name=u'ОТЦ Петель/ниток')
    # контрастные детали
    contrast_detail_collar = fields.Field(attribute='contrast_detail_collar', column_name=u'КТ Воротник')
    contrast_detail_collar_face = fields.Field(attribute='contrast_detail_collar_face',
                                               column_name=u'КТ Воротник лицевая сторона')
    contrast_detail_collar_bottom = fields.Field(attribute='contrast_detail_collar_bottom',
                                                 column_name=u'КТ Воротник низ')
    contrast_detail_collar_outer = fields.Field(attribute='contrast_detail_collar_outer',
                                                column_name=u'КТ Воротник внешняя стойка')
    contrast_detail_collar_inner = fields.Field(attribute='contrast_detail_collar_inner',
                                                column_name=u'КТ Воротник внутренняя стойка')
    contrast_detail_cuuff = fields.Field(attribute='contrast_detail_cuff', column_name=u'КТ Манжета')
    contrast_detail_cuff_outer = fields.Field(attribute='contrast_detail_cuff_outer',
                                              column_name=u'КТ Манжета внешняя')
    contrast_detail_cuff_inner = fields.Field(attribute='contrast_detail_cuff_inner',
                                              column_name=u'КТ Манжета внутренняя')

    export_headers = [u'Shirt Code', u'Код ткани', u'Коллекция', u'Пол', u'Размер', u'№ размера', u'Тип воротника',
                      u'Размер воротника', u'Жесткость воротника', u'Косточки', u'Манжеты', u'Вид манжеты', u'Рукав',
                      u'Жесткость манжеты', u'Низ', u'Полочка', u'Карман', u'Вытачки', u'Спинка', u'Вариант пуговиц',
                      u'Пуговицы', u'Код цвета пуговицы', u'Отстрочка (цвет)', u'ОТЦ Сорочка', u'ОТЦ Манжеты',
                      u'ОТЦ Воротник', u'ОТЦ Петель/ниток', u'Отстрочка (мм)', u'Цельная кокетка',
                      u'Застежка под штифты', u'Манишка', u'МА Ткань', u'МА Тип', u'Контрастные ткани', u'КТ Воротник',
                      u'КТ Воротник лицевая сторона', u'КТ Воротник низ', u'КТ Воротник внешняя стойка',
                      u'КТ Воротник внутренняя стойка', u'КТ Манжета', u'КТ Манжета внешняя', u'КТ Манжета внутренняя',
                      u'Инициалы', u'ИН Шрифт', u'ИН Цвет', u'ИН Позиция', ]

    class Meta:
        model = TemplateShirt
        import_id_fields = ('code',)
        fields = ('code',)
        skip_unchanged = True
        select_related = ['fabric', 'collection', 'collar__type', 'collar__hardness', 'collar__stays', 'collar__size',
                      'shirt_cuff__type', 'shirt_cuff__rounding', 'shirt_cuff__hardness', 'hem',
                      'placket', 'pocket', 'back', 'custom_buttons_type', 'custom_buttons', 'yoke', 'dickey__fabric',
                      'dickey__type', 'initials__font', 'initials__color']
        prefetch_related = ['contrast_stitches', 'shirt_contrast_details']
        instance_loader_class = CachedWithPrefetchedInstanceLoader.prepare(select_related, prefetch_related)


    def get_queryset(self):
        qs = super(TemplateShirtResource, self).get_queryset()
        return qs.select_related(*self._meta.select_related).prefetch_related(*self._meta.prefetch_related)

    def export(self, queryset=None):
        queryset = self.get_queryset().iterator()
        data = tablib.Dataset(headers=self.export_headers)
        for obj in queryset:
            row = [
                obj.code,
                obj.fabric.code,
                obj.collection.title if obj.collection else '',
                obj.collection.get_sex_display() if obj.collection else '',
                obj.size_option.title,
                obj.size.size if obj.size else '',
            ]

            # Воротник
            if hasattr(obj, 'collar'):
                row.append(obj.collar.type.title)
                row.append(obj.collar.size.title)
                if obj.collar.hardness:
                    row.append(obj.collar.hardness.title)
                else:
                    row.append('')
                if obj.collar.stays:
                    row.append(obj.collar.stays.title)
                else:
                    row.append('')
            else:
                row += ['' for i in range(4)]

            # Манжета
            if hasattr(obj, 'shirt_cuff'):
                row.append(obj.shirt_cuff.type.title)
                if obj.shirt_cuff.rounding:
                    row.append(obj.shirt_cuff.rounding.title)
                else:
                    row.append('')
                # пропускаем рукав
                row.append('')
                if obj.shirt_cuff.hardness:
                    row.append(obj.shirt_cuff.hardness.title)
                else:
                    row.append('')
            else:
                row += ['' for i in range(4)]

            # Рукав
            row[-2] = obj.sleeve.title if hasattr(obj, 'sleeve') else ''

            row += [
                obj.hem.title,
                obj.placket.title,
                obj.pocket.title,
                obj.get_tuck_display(),
                obj.back.title,
            ]

            # Кастомные пуговицы
            if obj.custom_buttons_type:
                row += [
                    self.BUTTONS_DEFAULT_DICT[True],
                    obj.custom_buttons_type.title,
                    obj.custom_buttons.title,
                ]
            else:
                row += ['' for i in range(3)]

            # Контрастные отстрочки
            row.append(self.CONTRAST_STITCHES_USE_DICT[len(obj.contrast_stitches.all()) > 0])
            row += [
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == u'Сорочка'), ''),
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == u'Манжета'), ''),
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == u'Воротник'), ''),
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == u'Петели/нитки'), ''),
            ]

            row += [
                obj.get_stitch_display(),
                obj.yoke.title if obj.yoke else '',
            ]
            row.append(self.CLASP_USE_DICT[obj.clasp is not None])
            # Манишка
            row.append(self.DICKEY_USE_DICT[obj.dickey is not None])
            if obj.dickey:
                row += [
                    obj.dickey.fabric.code,
                    obj.dickey.type.title,
                ]
            else:
                row += ['' for i in range(2)]

            # Контрастные ткани
            row.append(self.SHIRT_CONTRAST_DETAILS_USE_DICT[len(obj.shirt_contrast_details.all()) > 0])
            row += [
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar_face'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar_bottom'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar_outer'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar_inner'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'cuff'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'cuff_outer'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'cuff_inner'), ''),
            ]

            # Инициалы
            row.append(self.INITIALS_USE_DICT[obj.initials is not None])
            if obj.initials:
                if obj.initials.font:
                    row.append(obj.initials.font.title)
                else:
                    row.append('')
                row += [
                    obj.initials.color.title,
                    obj.initials.get_location_display(),
                ]
            else:
                row += ['' for i in range(3)]

            data.append(row)
        return data

    def import_contrast_stitch(self, instance, element, color):
        if color:
            try:
                detail = ContrastStitch.objects.get(
                    element=ElementStitch.objects.get_or_create(title=element)[0],
                    shirt=instance
                )
                detail.color = dictionaries.StitchColor.objects.get_or_create(title=color)[0]
                detail.save()
            except ContrastStitch.DoesNotExist:
                ContrastStitch.objects.create(
                    element=ElementStitch.objects.get_or_create(title=element)[0],
                    color=dictionaries.StitchColor.objects.get_or_create(title=color)[0],
                    shirt=instance
                )
        else:
            self.remove_contrast_stich(instance, element)

    def remove_contrast_stich(self, instance, element):
        try:
            detail = ContrastStitch.objects.filter(element=ElementStitch.objects.get_or_create(title=element)[0],
                                                   shirt=instance)
            detail.delete()
        except ContrastStitch.DoesNotExist:
            pass

    def import_contrast_detail(self, instance, element, fabric):
        if fabric:
            try:
                detail = ContrastDetails.objects.get(
                    element=element,
                    shirt=instance
                )
                detail.fabric = Fabric.objects.get_or_create(code=fabric)[0]
                detail.save()
            except ContrastDetails.DoesNotExist:
                ContrastDetails.objects.create(
                    element=element,
                    fabric=Fabric.objects.get_or_create(code=fabric)[0],
                    shirt=instance
                )
        else:
            self.remove_contrast_stich(instance, element)

    def remove_contrast_detail(self, instance, element):
        try:
            detail = ContrastDetails.objects.filter(element=element, shirt=instance)
            detail.delete()
        except ContrastDetails.DoesNotExist:
            pass

    def before_save_instance(self, instance, dry_run):
        if not dry_run:
            save_relations(instance, 'fabric')
            save_relations(instance, 'collection')
            save_relations(instance, 'hem')
            save_relations(instance, 'placket')
            save_relations(instance, 'size_option')
            save_relations(instance, 'pocket')
            save_relations(instance, 'back')
            save_relations(instance, 'yoke')
            save_relations(instance, 'sleeve')
            save_relations(instance.collar, 'type')
            save_relations(instance.collar, 'hardness')
            save_relations(instance.collar, 'stays')
            save_relations(instance.collar, 'size')
            if hasattr(instance, 'shirt_cuff'):
                save_relations(instance.shirt_cuff, 'type')
                save_relations(instance.shirt_cuff, 'rounding')
                save_relations(instance.shirt_cuff, 'hardness')

            if instance.dickey is not None:
                save_relations(instance, 'dickey')
                save_relations(instance.dickey, 'type')
                save_relations(instance.dickey, 'fabric')

            if instance.initials is not None:
                save_relations(instance, 'initials')
                save_relations(instance.initials, 'font')
                save_relations(instance.initials, 'color')

            if instance.size is not None and instance.size._state.adding:
                instance.size.save()
                instance.size = instance.size

            if instance.initials is not None:
                try:
                    instance.initials.location = \
                        next(x for x in instance.initials.LOCATION if x[1] == instance.initials.location)[0]
                except StopIteration:
                    instance.initials.location = instance.initials.LOCATION.button2

    def after_save_instance(self, instance, dry_run):
        if not dry_run:
            instance.collar.shirt = instance
            save_relations(instance, 'collar')
            if hasattr(instance, 'shirt_cuff'):
                instance.shirt_cuff.shirt = instance
                save_relations(instance, 'shirt_cuff')

            # контрастные отстрочки
            self.import_contrast_stitch(instance, u'Сорочка', instance.contrast_stitch_shirt)
            self.import_contrast_stitch(instance, u'Манжета', instance.contrast_stitch_cuff)
            self.import_contrast_stitch(instance, u'Воротник', instance.contrast_stitch_collar)
            self.import_contrast_stitch(instance, u'Петели/нитки', instance.contrast_stitch_loops)
            # контрастные детали
            if instance.contrast_detail_collar:
                self.import_contrast_detail(instance, 'collar_face', instance.contrast_detail_collar)
                self.import_contrast_detail(instance, 'collar_bottom', instance.contrast_detail_collar)
                self.import_contrast_detail(instance, 'collar_outer', instance.contrast_detail_collar)
                self.import_contrast_detail(instance, 'collar_inner', instance.contrast_detail_collar)
            else:
                self.import_contrast_detail(instance, 'collar_face', instance.contrast_detail_collar_face)
                self.import_contrast_detail(instance, 'collar_bottom', instance.contrast_detail_collar_bottom)
                self.import_contrast_detail(instance, 'collar_outer', instance.contrast_detail_collar_outer)
                self.import_contrast_detail(instance, 'collar_inner', instance.contrast_detail_collar_inner)
            if instance.contrast_detail_cuff:
                self.import_contrast_detail(instance, 'cuff_outer', instance.contrast_detail_cuff)
                self.import_contrast_detail(instance, 'cuff_inner', instance.contrast_detail_cuff)
            else:
                self.import_contrast_detail(instance, 'cuff_outer', instance.contrast_detail_cuff_outer)
                self.import_contrast_detail(instance, 'cuff_inner', instance.contrast_detail_cuff_inner)

    def import_obj(self, obj, data, dry_run):
        if not hasattr(obj, 'collar'):
            obj.collar = Collar()
        if data[self.CUFF_COLUMN_NAME] and not hasattr(obj, 'shirt_cuff'):
            obj.shirt_cuff = Cuff()

        if data[self.INITIALS_COLUMN_NAME] != self.INITIALS_USE_DICT[False] and obj.initials is None:
            obj.initials = Initials()
        use_dickey = self.DICKEY_USE_DICT[True] in data[self.DICKEY_COLUMN_NAME]
        if use_dickey:
            obj.dickey = Dickey()
        if data[self.INITIALS_COLUMN_NAME] == self.INITIALS_USE_DICT[True] and obj.initials is None:
            obj.initials = Initials()
        for field in self.get_fields():
            if isinstance(field.widget, ManyToManyWidget):
                continue
            self.import_field(field, obj, data)

    def import_field(self, field, obj, data):
        if field.attribute and field.column_name in data:
            if field.attribute in self.COLLECTION_ATTRIBUTE_MAP:
                field.save(obj, data, sex=data[self.SEX_COLUMN_NAME])
            elif field.attribute in self.TUCK_ATTRIBUTE_MAP:
                obj.tuck = data[self.TUCK_COLUMN_NAME] != self.TUCK_NOT_USE_CONSTANT
            elif field.attribute in self.CLASP_ATTRIBUTE_MAP:
                obj.clasp = data[self.CLASP_COLUMN_NAME] == self.CLASP_USE_DICT[True]
            elif field.attribute in self.DICKEY_ATTRIBUTE_MAP:
                use_dickey = self.DICKEY_USE_DICT[True] in data[self.DICKEY_COLUMN_NAME]
                if use_dickey:
                    field.save(obj, data)
            elif field.attribute in self.INITIALS_ATTRIBUTE_MAP:
                if data[self.INITIALS_COLUMN_NAME] != self.INITIALS_USE_DICT[False]:
                    field.save(obj, data)
            elif field.attribute in self.CUFF_ATTRIBUTE_LIST:
                if hasattr(obj, 'shirt_cuff'):
                    field.save(obj, data)
            else:
                field.save(obj, data)
        else:
            return None
