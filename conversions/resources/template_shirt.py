# coding: utf-8

import tablib
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from import_export import fields
from import_export import resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from backend.models import Fabric, TemplateShirt, Collection, Collar, Hardness, Stays, Cuff, CustomButtons, Dickey, \
    Initials, ContrastStitch, ElementStitch, ContrastDetails, ShawlOptions
from conversions.fields import TemplateShirtCollectionField
from conversions.instance_loaders import CachedWithPrefetchedInstanceLoader
from conversions.utils import save_relations
from conversions.widgets import CustomForeignKeyWidget, TemplateShirtCollectionWidget, ChoicesWidget
from core.utils import first
from dictionaries import models as dictionaries


class TemplateShirtResource(resources.ModelResource):
    BUTTONS_DEFAULT_DICT = {
        True: _(u'Пожалуйста, используйте стандартные пуговицы'),
        False: u''
    }
    CONTRAST_STITCHES_USE_DICT = {
        True: _(u'Я хочу использовать отстрочку контрастного цвета'),
        False: _(u'Я не хочу использовать отстрочку контрастного цвета')
    }
    CLASP_USE_DICT = {
        True: _(u'Я хочу использовать застежку под штифты'),
        False: _(u'Я не хочу использовать застежку под штифты'),
    }
    DICKEY_USE_DICT = {
        True: _(u'Я хочу использовать манишку'),
        False: _(u'Я не хочу использовать манишку'),
    }
    CONTRAST_DETAILS_USE_DICT = {
        True: _(u'Я хочу использовать контрастные ткани'),
        False: _(u'Я не хочу использовать контрастные ткани'),
    }
    INITIALS_USE_DICT = {
        True: _(u'Я хочу использовать инициалы'),
        False: _(u'Я не хочу использовать инициалы')
    }

    COLLECTION_ATTRIBUTE_MAP = {'collection'}
    CLASP_ATTRIBUTE_MAP = {'clasp'}
    CUFF_ATTRIBUTE_LIST = ('cuff__type', 'cuff__rounding', 'cuff__hardness')
    DICKEY_ATTRIBUTE_MAP = {'dickey__type', 'dickey__fabric'}
    INITIALS_ATTRIBUTE_MAP = {'initials__font', 'initials__color', 'initials__location'}
    INITIALS_CHOICES_ATTRIBUTE_MAP = {'initials__location'}

    SEX_COLUMN_NAME = _(u'Пол')
    TUCK_COLUMN_NAME = _(u'Вытачки')
    CLASP_COLUMN_NAME = _(u'Застежка под штифты')
    DICKEY_COLUMN_NAME = _(u'Манишка')
    CUFF_COLUMN_NAME = _(u'Манжеты')
    INITIALS_COLUMN_NAME = _(u'Инициалы')

    code = fields.Field(attribute='code', column_name='Shirt Code')
    fabric = fields.Field(attribute='fabric', column_name=_(u'Код ткани'),
                          widget=CustomForeignKeyWidget(Fabric, field='code'))
    size_option = fields.Field(attribute='size_option', column_name=_(u'Размер'),
                               widget=CustomForeignKeyWidget(model=dictionaries.SizeOptions, field='title'))
    size = fields.Field(attribute='size', column_name=_(u'№ размера'),
                        widget=CustomForeignKeyWidget(model=dictionaries.Size, field='size'))
    hem = fields.Field(attribute='hem', column_name=_(u'Низ'),
                       widget=CustomForeignKeyWidget(model=dictionaries.HemType, field='title'))
    placket = fields.Field(attribute='placket', column_name=_(u'Полочка'),
                           widget=CustomForeignKeyWidget(model=dictionaries.PlacketType, field='title'))
    pocket = fields.Field(attribute='pocket', column_name=_(u'Карман'),
                          widget=CustomForeignKeyWidget(model=dictionaries.PocketType, field='title'))
    tuck = fields.Field(attribute='tuck', column_name=TUCK_COLUMN_NAME,
                        widget=CustomForeignKeyWidget(model=dictionaries.TuckType, field='title'))
    back = fields.Field(attribute='back', column_name=_(u'Спинка'),
                        widget=CustomForeignKeyWidget(model=dictionaries.BackType, field='title'))
    collection = TemplateShirtCollectionField(attribute='collection', column_name=_(u'Коллекция'),
                                              widget=TemplateShirtCollectionWidget(Collection, field='title'))
    stitch = fields.Field(attribute='stitch', column_name=_(u'Отстрочка (мм)'),
                          widget=ChoicesWidget(choices=TemplateShirt.STITCH))
    yoke = fields.Field(attribute='yoke', column_name=_(u'Цельная кокетка'),
                        widget=CustomForeignKeyWidget(dictionaries.YokeType, field='title'))
    clasp = fields.Field(attribute='clasp', column_name=CLASP_COLUMN_NAME, widget=ChoicesWidget(choices=CLASP_USE_DICT))
    sleeve = fields.Field(attribute='sleeve', column_name=_(u'Рукав'),
                          widget=CustomForeignKeyWidget(model=dictionaries.SleeveType, field='title'))
    # Импорт воротника
    collar__type = fields.Field(attribute='collar__type', column_name=_(u'Тип воротника'),
                                widget=CustomForeignKeyWidget(model=dictionaries.CollarType, field='title'))
    collar__hardness = fields.Field(attribute='collar__hardness', column_name=_(u'Жесткость воротника'),
                                    widget=CustomForeignKeyWidget(model=Hardness, field='title'))
    collar__stays = fields.Field(attribute='collar__stays', column_name=_(u'Косточки'),
                                 widget=CustomForeignKeyWidget(model=Stays, field='title'))
    collar__size = fields.Field(attribute='collar__size', column_name=_(u'Размер воротника'),
                                widget=CustomForeignKeyWidget(model=dictionaries.CollarButtons, field='title'))

    # Импорт манжеты
    cuff__type = fields.Field(attribute='cuff__type', column_name=CUFF_COLUMN_NAME,
                              widget=CustomForeignKeyWidget(model=dictionaries.CuffType, field='title'))
    cuff__rounding = fields.Field(attribute='cuff__rounding', column_name=_(u'Вид манжеты'),
                                  widget=CustomForeignKeyWidget(model=dictionaries.CuffRounding, field='title'))
    cuff__hardness = fields.Field(attribute='cuff__hardness', column_name=_(u'Жесткость манжеты'),
                                  widget=CustomForeignKeyWidget(model=Hardness, field='title'))
    # Импорт пуговиц
    custom_buttons_type = fields.Field(attribute='custom_buttons_type', column_name=_(u'Пуговицы'),
                                       widget=CustomForeignKeyWidget(model=dictionaries.CustomButtonsType,
                                                                     field='title'))
    custom_buttons = fields.Field(attribute='custom_buttons', column_name=_(u'Код цвета пуговицы'),
                                  widget=CustomForeignKeyWidget(model=CustomButtons, field='title'))
    # импорт манишки
    dickey__type = fields.Field(attribute='dickey__type', column_name=_(u'МА Тип'),
                                widget=CustomForeignKeyWidget(dictionaries.DickeyType, field='title'))
    dickey__fabric = fields.Field(attribute='dickey__fabric', column_name=_(u'МА Ткань'),
                                  widget=CustomForeignKeyWidget(Fabric, field='code'))
    # импорт инициалов
    initials__font = fields.Field(attribute='initials__font', column_name=_(u'ИН Шрифт'),
                                  widget=ForeignKeyWidget(dictionaries.Font, field='title'))
    initials__color = fields.Field(attribute='initials__color', column_name=_(u'ИН Цвет'),
                                   widget=ForeignKeyWidget(dictionaries.Color, field='title'))
    initials__location = fields.Field(attribute='initials__location', column_name=_(u'ИН Позиция'))
    # контрастные отстрочки
    contrast_stitch_shirt = fields.Field(attribute='contrast_stitch_shirt', column_name=_(u'ОТЦ Сорочка'))
    contrast_stitch_cuff = fields.Field(attribute='contrast_stitch_cuff', column_name=_(u'ОТЦ Манжеты'))
    contrast_stitch_collar = fields.Field(attribute='contrast_stitch_collar', column_name=_(u'ОТЦ Воротник'))
    contrast_stitch_loops = fields.Field(attribute='contrast_stitch_loops', column_name=_(u'ОТЦ Петель/ниток'))
    # контрастные детали
    contrast_detail_collar = fields.Field(attribute='contrast_detail_collar', column_name=_(u'КТ Воротник'))
    contrast_detail_collar_face = fields.Field(attribute='contrast_detail_collar_face',
                                               column_name=_(u'КТ Воротник лицевая сторона'))
    contrast_detail_collar_bottom = fields.Field(attribute='contrast_detail_collar_bottom',
                                                 column_name=_(u'КТ Воротник низ'))
    contrast_detail_collar_outer = fields.Field(attribute='contrast_detail_collar_outer',
                                                column_name=_(u'КТ Воротник внешняя стойка'))
    contrast_detail_collar_inner = fields.Field(attribute='contrast_detail_collar_inner',
                                                column_name=_(u'КТ Воротник внутренняя стойка'))
    contrast_detail_cuff = fields.Field(attribute='contrast_detail_cuff', column_name=_(u'КТ Манжета'))
    contrast_detail_cuff_outer = fields.Field(attribute='contrast_detail_cuff_outer',
                                              column_name=_(u'КТ Манжета внешняя'))
    contrast_detail_cuff_inner = fields.Field(attribute='contrast_detail_cuff_inner',
                                              column_name=_(u'КТ Манжета внутренняя'))

    export_headers = [_(u'Shirt Code'), _(u'Код ткани'), _(_(u'Коллекция')), _(_(u'Пол')), _(_(u'Размер')),
                      _(_(u'№ размера')), _(u'Тип воротника'),
                      _(u'Размер воротника'), _(u'Жесткость воротника'), _(u'Косточки'), _(u'Манжеты'),
                      _(u'Вид манжеты'), _(u'Рукав'),
                      _(u'Жесткость манжеты'), _(u'Низ'), _(u'Полочка'), _(u'Карман'), _(u'Вытачки'), _(u'Спинка'),
                      _(u'Вариант пуговиц'),
                      _(u'Пуговицы'), _(u'Код цвета пуговицы'), _(u'Отстрочка (цвет)'), _(u'ОТЦ Сорочка'),
                      _(u'ОТЦ Манжеты'),
                      _(u'ОТЦ Воротник'), _(u'ОТЦ Петель/ниток'), _(u'Отстрочка (мм)'), _(u'Цельная кокетка'),
                      _(u'Застежка под штифты'), _(u'Манишка'), _(u'МА Ткань'), _(u'МА Тип'), _(u'Контрастные ткани'),
                      _(u'КТ Воротник'),
                      _(u'КТ Воротник лицевая сторона'), _(u'КТ Воротник низ'), _(u'КТ Воротник внешняя стойка'),
                      _(u'КТ Воротник внутренняя стойка'), _(u'КТ Манжета'), _(u'КТ Манжета внешняя'),
                      _(u'КТ Манжета внутренняя'),
                      _(u'Инициалы'), _(u'ИН Шрифт'), _(u'ИН Цвет'), _(u'ИН Позиция')]

    class Meta:
        model = TemplateShirt
        import_id_fields = ('code',)
        fields = ('code',)
        skip_unchanged = True
        select_related = ['fabric', 'collection', 'collar__type', 'collar__hardness', 'collar__stays', 'collar__size',
                          'cuff__type', 'cuff__rounding', 'cuff__hardness', 'hem',
                          'placket', 'pocket', 'back', 'custom_buttons_type', 'custom_buttons', 'yoke',
                          'dickey__fabric', 'tuck', 'sleeve', 'size_option', 'size',
                          'dickey__type', 'initials__font', 'initials__color']
        prefetch_related = ['contrast_stitches', 'contrast_details', 'dickey']
        instance_loader_class = CachedWithPrefetchedInstanceLoader.prepare(select_related, prefetch_related)

    @cached_property
    def stitch_elements(self):
        return ElementStitch.objects.values('id', 'title')

    @cached_property
    def stitch_colors(self):
        return dictionaries.StitchColor.objects.values('id', 'title')

    @cached_property
    def fabrics(self):
        return list(Fabric.objects.all())

    @cached_property
    def defaults(self):
        return {
            'sleeve': dictionaries.resolve_default_object(dictionaries.SleeveType),
            'shawl': dictionaries.resolve_default_object(ShawlOptions)
        }

    def get_queryset(self):
        qs = super(TemplateShirtResource, self).get_queryset()
        return qs.select_related(*self._meta.select_related).prefetch_related(*self._meta.prefetch_related)

    def export(self, queryset=None, *args, **kwargs):
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
            if hasattr(obj, 'cuff'):
                row.append(obj.cuff.type.title)
                if obj.cuff.rounding:
                    row.append(obj.cuff.rounding.title)
                else:
                    row.append('')
                # пропускаем рукав
                row.append('')
                if obj.cuff.hardness:
                    row.append(obj.cuff.hardness.title)
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
                obj.tuck.title,
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
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == _(u'Сорочка')), ''),
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == _(u'Манжета')), ''),
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == _(u'Воротник')), ''),
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == _(u'Петели/нитки')), ''),
            ]

            row += [
                obj.get_stitch_display(),
                obj.yoke.title if obj.yoke else '',
            ]
            row.append(self.CLASP_USE_DICT[obj.clasp is not None])
            # Манишка
            dickey = getattr(obj, 'dickey', None)
            row.append(self.DICKEY_USE_DICT[dickey is not None])
            if dickey:
                row += [
                    dickey.fabric.code,
                    dickey.type.title,
                ]
            else:
                row += ['' for i in range(2)]

            # Контрастные ткани
            row.append(self.CONTRAST_DETAILS_USE_DICT[len(obj.contrast_details.all()) > 0])
            row += [
                next((x.fabric.code for x in obj.contrast_details.all() if x.element == 'collar'), ''),
                next((x.fabric.code for x in obj.contrast_details.all() if x.element == 'collar_face'), ''),
                next((x.fabric.code for x in obj.contrast_details.all() if x.element == 'collar_bottom'), ''),
                next((x.fabric.code for x in obj.contrast_details.all() if x.element == 'collar_outer'), ''),
                next((x.fabric.code for x in obj.contrast_details.all() if x.element == 'collar_inner'), ''),
                next((x.fabric.code for x in obj.contrast_details.all() if x.element == 'cuff'), ''),
                next((x.fabric.code for x in obj.contrast_details.all() if x.element == 'cuff_outer'), ''),
                next((x.fabric.code for x in obj.contrast_details.all() if x.element == 'cuff_inner'), ''),
            ]

            # Инициалы
            has_initials = hasattr(obj, 'initials')
            row.append(self.INITIALS_USE_DICT[has_initials])
            if has_initials:
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
        if instance.marked_new:
            stitch = None
        else:
            stitch = first(lambda cs: cs.element.title == element, instance.contrast_stitches.all())
        if color:
            element = first(lambda e: e['title'] == element, self.stitch_elements)
            color = first(lambda c: c['title'] == color, self.stitch_colors)
            if stitch is None:
                stitch = ContrastStitch(shirt=instance, element_id=element['id'], color_id=color['id'])
            stitch.save()
        elif stitch is not None:
            stitch.delete()

    def import_contrast_detail(self, instance, element, fabric_code):
        if instance.marked_new:
            detail = None
        else:
            detail = first(lambda cd: cd.element == element, instance.contrast_details.all())
        if fabric_code:
            fabric = first(lambda f: f.code == fabric_code, self.fabrics)
            assert fabric is not None, 'Could find fabric with the following fabric code: %s' % fabric_code
            if detail is None:
                detail = ContrastDetails(shirt=instance, element=element, fabric=fabric)
            # ignore pricing for now
            detail.ignore_signals = True
            detail.save()
        elif detail is not None:
            detail.delete()

    def before_save_instance(self, instance, dry_run):
        if not dry_run:
            instance.marked_new = instance.pk is None

            if instance.size is not None and instance.size._state.adding:
                instance.size.save()
                instance.size = instance.size

            if hasattr(instance, 'initials'):
                try:
                    instance.initials.location = \
                        next(x for x in instance.initials.LOCATION if x[1] == instance.initials.location)[0]
                except StopIteration:
                    instance.initials.location = instance.initials.LOCATION.button2

    def save_related(self, shirt, field):
        entity = getattr(shirt, field, None)
        if not entity:
            return
        entity.shirt = shirt
        save_relations(shirt, field)

    def after_save_instance(self, instance, dry_run):
        if not dry_run:
            self.save_related(instance, 'collar')
            self.save_related(instance, 'cuff')
            self.save_related(instance, 'dickey')
            self.save_related(instance, 'initials')

            # контрастные отстрочки
            self.import_contrast_stitch(instance, _(u'Сорочка'), instance.contrast_stitch_shirt)
            self.import_contrast_stitch(instance, _(u'Манжета'), instance.contrast_stitch_cuff)
            self.import_contrast_stitch(instance, _(u'Воротник'), instance.contrast_stitch_collar)
            self.import_contrast_stitch(instance, _(u'Петели/нитки'), instance.contrast_stitch_loops)
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
        if data[self.CUFF_COLUMN_NAME] and not hasattr(obj, 'cuff'):
            obj.cuff = Cuff()

        if data[self.INITIALS_COLUMN_NAME] != self.INITIALS_USE_DICT[False] and not hasattr(obj, 'initials'):
            obj.initials = Initials()
        use_dickey = self.DICKEY_USE_DICT[True] in data[self.DICKEY_COLUMN_NAME]
        if use_dickey and not hasattr(obj, 'dickey'):
            obj.dickey = Dickey()
        for field in self.get_fields():
            if isinstance(field.widget, ManyToManyWidget):
                continue
            self.import_field(field, obj, data)

    def import_field(self, field, obj, data):
        if field.attribute and field.column_name in data:
            if field.attribute in self.COLLECTION_ATTRIBUTE_MAP:
                field.save(obj, data, sex=data[self.SEX_COLUMN_NAME])
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
                if hasattr(obj, 'cuff'):
                    field.save(obj, data)
            else:
                field.save(obj, data)
        else:
            return None

    def init_instance(self, row=None):
        return self._meta.model(**self.defaults)
