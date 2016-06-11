# coding: utf-8
from __future__ import absolute_import

import tablib

from diff_match_patch import diff_match_patch
from django.db.models import QuerySet
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from backend.import_export.fields import TemplateShirtCollectionField
from backend.import_export.utils import save_relations
from backend.import_export.widgets import CustomForeignKeyWidget, TemplateShirtCollectionWidget
from backend.models import Fabric, TemplateShirt, Collection, Collar, Hardness, Stays, Cuff, CustomButtons, Dickey, \
    Initials, ContrastStitch, ElementStitch, ContrastDetails
from dictionaries import models as dictionaries


class TemplateShirtResource(resources.ModelResource):
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
    tuck = fields.Field(attribute='tuck', column_name=u'Вытачки')
    back = fields.Field(attribute='back', column_name=u'Спинка',
                        widget=CustomForeignKeyWidget(model=dictionaries.BackType, field='title'))
    collection = TemplateShirtCollectionField(attribute='collection', column_name=u'Коллекция',
                                              widget=TemplateShirtCollectionWidget(Collection, field='title'))
    stitch = fields.Field(attribute='stitch', column_name=u'Отстрочка (мм)')
    yoke = fields.Field(attribute='yoke', column_name=u'Цельная кокетка',
                        widget=CustomForeignKeyWidget(dictionaries.YokeType, field='title'))
    clasp = fields.Field(attribute='clasp', column_name=u'Застежка под штифты')
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
    shirt_cuff__type = fields.Field(attribute='shirt_cuff__type', column_name=u'Манжеты',
                                    widget=CustomForeignKeyWidget(model=dictionaries.CuffType, field='title'))
    shirt_cuff__rounding = fields.Field(attribute='shirt_cuff__rounding', column_name=u'Вид манжеты',
                                        widget=CustomForeignKeyWidget(model=dictionaries.CuffRounding, field='title'))
    shirt_cuff__sleeve = fields.Field(attribute='shirt_cuff__sleeve', column_name=u'Рукав',
                                      widget=CustomForeignKeyWidget(model=dictionaries.SleeveType, field='title'))
    shirt_cuff__hardness = fields.Field(attribute='shirt_cuff__hardness', column_name=u'Жесткость манжеты',
                                        widget=CustomForeignKeyWidget(model=Hardness, field='title'))
    # Импорт пуговиц
    custom_buttons_type = fields.Field(attribute='custom_buttons_type', column_name=u'Вариант пуговиц',
                                       widget=ForeignKeyWidget(model=dictionaries.CustomButtonsType, field='title'))
    custom_buttons = fields.Field(attribute='custom_buttons', column_name=u'Пуговицы',
                                  widget=ForeignKeyWidget(model=CustomButtons, field='title'))
    # импорт манишки
    dickey__type = fields.Field(attribute='dickey__type', column_name=u'МА Тип',
                                widget=ForeignKeyWidget(dictionaries.DickeyType, field='title'))
    dickey__fabric = fields.Field(attribute='dickey__fabric', column_name=u'МА Ткань',
                                  widget=ForeignKeyWidget(Fabric, field='code'))
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
    contrast_detail_collar_face = fields.Field(attribute='contrast_detail_collar_face', column_name=u'КТ Воротник лицевая сторона')
    contrast_detail_collar_bottom = fields.Field(attribute='contrast_detail_collar_bottom', column_name=u'КТ Воротник низ')
    contrast_detail_collar_outer = fields.Field(attribute='contrast_detail_collar_outer', column_name=u'КТ Воротник внешняя стойка')
    contrast_detail_collar_inner = fields.Field(attribute='contrast_detail_collar_inner', column_name=u'КТ Воротник внутренняя стойка')
    contrast_detail_cuuff = fields.Field(attribute='contrast_detail_cuff', column_name=u'КТ Манжета')
    contrast_detail_cuff_outer = fields.Field(attribute='contrast_detail_cuff_outer', column_name=u'КТ Манжета внешняя')
    contrast_detail_cuff_inner = fields.Field(attribute='contrast_detail_cuff_inner', column_name=u'КТ Манжета внутренняя')

    select_related = ('fabric', 'collection', 'collar__type', 'collar__hardness', 'collar__stays', 'collar__size',
                      'shirt_cuff__type', 'shirt_cuff__rounding', 'shirt_cuff__sleeve', 'shirt_cuff__hardness', 'hem',
                      'placket', 'pocket', 'back', 'custom_buttons_type', 'custom_buttons', 'yoke', 'dickey__fabric',
                      'dickey__type', 'initials__font', 'initials__color', )
    prefetch_related = ('contrast_stitches', 'shirt_contrast_details', )

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
        import_id_fields = ('code', )
        fields = ('code', )

    def get_queryset(self):
        qs = super(TemplateShirtResource, self).get_queryset()
        return qs.select_related(*self.select_related).prefetch_related(*self.prefetch_related)

    def export(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        data = tablib.Dataset(headers=self.export_headers)

        if isinstance(queryset, QuerySet):
            iterable = queryset.iterator()
        else:
            iterable = queryset
        for obj in iterable:
            row = [
                obj.code,
                obj.fabric.code,
                obj.collection.title if obj.collection else '',
                obj.collection.get_sex_display() if obj.collection else '',
                obj.size_option.title,
                obj.size.size if obj.size else '',
                # TODO: упросить запись row
                obj.collar.type.title if hasattr(obj, 'collar') else '',
                obj.collar.size.title if hasattr(obj, 'collar') else '',
                obj.collar.hardness.title if hasattr(obj, 'collar') and obj.collar.hardness else '',
                obj.collar.stays.title if hasattr(obj, 'collar') and obj.collar.stays else '',
                obj.shirt_cuff.type.title if hasattr(obj, 'shirt_cuff') else '',
                obj.shirt_cuff.rounding.title if hasattr(obj, 'shirt_cuff') and obj.shirt_cuff.rounding else '',
                obj.shirt_cuff.sleeve.title if hasattr(obj, 'shirt_cuff') else '',
                obj.shirt_cuff.hardness.title if hasattr(obj, 'shirt_cuff') and obj.shirt_cuff.hardness else '',
                obj.hem.title,
                obj.placket.title,
                obj.pocket.title,
                obj.get_tuck_display(),
                obj.back.title,
                obj.custom_buttons_type.title if obj.custom_buttons_type else '',
                obj.custom_buttons.title if obj.custom_buttons else '',
                '', # TODO подписать
                u'Я хочу использовать отстрочку контрастного цвета' if obj.contrast_stitches.all() else u'Я не хочу использовать отстрочку контрастного цвета',
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == u'Сорочка'), ''),
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == u'Манжета'), ''),
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == u'Воротник'), ''),
                next((x.color.title for x in obj.contrast_stitches.all() if x.element.title == u'Петели/нитки'), ''),
                obj.get_stitch_display(),
                obj.yoke.title if obj.yoke else '',
                u'Я хочу использовать застежку под штифты' if obj.clasp else u'Я не хочу использовать застежку под штифты',
                u'Я хочу использовать манишку' if obj.dickey else u'Я не хочу использовать манишку',
                obj.dickey.fabric.code if obj.dickey else '',
                obj.dickey.type.title if obj.dickey else '',
                u'Я хочу использовать контрастные ткани' if obj.shirt_contrast_details.all() else u'Я не хочу использовать контрастные ткани',
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar_face'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar_bottom'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar_outer'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'collar_inner'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'cuff'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'cuff_outer'), ''),
                next((x.fabric.code for x in obj.shirt_contrast_details.all() if x.element == 'cuff_inner'), ''),
                u'Я хочу использовать инициалы' if obj.initials else u'Я не хочу использовать инициалы',
                obj.initials.font.title if obj.initials and obj.initials.font else '',
                obj.initials.color.title if obj.initials else '',
                obj.initials.get_location_display() if obj.initials else '',
            ]
            data.append(row)
        return data

    def import_contrast_stich(self, instance, element, color):
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
            detail = ContrastStitch.objects.filter(element=ElementStitch.objects.get_or_create(title=element)[0], shirt=instance)
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
            save_relations(instance.collar, 'type')
            save_relations(instance.collar, 'hardness')
            save_relations(instance.collar, 'stays')
            save_relations(instance.collar, 'size')
            if instance.dickey is not None:
                save_relations(instance, 'dickey')
                save_relations(instance.dickey, 'type')
                save_relations(instance.dickey, 'fabric')
            if instance.initials is not None:
                save_relations(instance, 'initials')
                save_relations(instance.initials, 'font')
                save_relations(instance.initials, 'color')
            save_relations(instance.shirt_cuff, 'type')
            save_relations(instance.shirt_cuff, 'rounding')
            save_relations(instance.shirt_cuff, 'sleeve')
            save_relations(instance.shirt_cuff, 'hardness')

            if instance.size is not None and instance.size._state.adding:
                instance.size.save()
                instance.size = instance.size

            try:
                instance.stitch = next(x for x in instance.STITCH if x[1] == instance.stitch)[0]
            except StopIteration:
                instance.stitch = 'none' # TODO: через choice

            if instance.initials is not None:
                try:
                    instance.initials.location = next(x for x in instance.initials.LOCATION if x[1] == instance.initials.location)[0]
                except StopIteration:
                    instance.initials.location = 'button2' # TODO: через choice

    def after_save_instance(self, instance, dry_run):
        if not dry_run:
            instance.collar.shirt = instance
            save_relations(instance, 'collar')
            instance.shirt_cuff.shirt = instance
            save_relations(instance, 'shirt_cuff')

            # контрастные отстрочки
            self.import_contrast_stich(instance, u'Сорочка', instance.contrast_stitch_shirt)
            self.import_contrast_stich(instance, u'Манжета', instance.contrast_stitch_cuff)
            self.import_contrast_stich(instance, u'Воротник', instance.contrast_stitch_collar)
            self.import_contrast_stich(instance, u'Петели/нитки', instance.contrast_stitch_loops)
            # контрастные детали
            self.import_contrast_detail(instance, 'collar', instance.contrast_detail_collar) # TODO: выкинуть
            self.import_contrast_detail(instance, 'collar_face', instance.contrast_detail_collar_face)
            self.import_contrast_detail(instance, 'collar_bottom', instance.contrast_detail_collar_bottom)
            self.import_contrast_detail(instance, 'collar_outer', instance.contrast_detail_collar_outer)
            self.import_contrast_detail(instance, 'collar_inner', instance.contrast_detail_collar_inner)
            self.import_contrast_detail(instance, 'cuff', instance.contrast_detail_cuff) # TODO: выкинуть
            self.import_contrast_detail(instance, 'cuff_outer', instance.contrast_detail_cuff_outer)
            self.import_contrast_detail(instance, 'cuff_inner', instance.contrast_detail_cuff_inner)

    def import_obj(self, obj, data, dry_run):
        try:
            obj.collar
        except:
            obj.collar = Collar()
        try:
            obj.shirt_cuff
        except:
            obj.shirt_cuff = Cuff()
        if data[u'Манишка'] != u'Я не хочу использовать манишку' and obj.dickey is None: # TODO: выкинуть
            obj.dickey = Dickey()
        if data[u'Инициалы'] != u'Я не хочу использовать инициалы' and obj.initials is None: # TODO: выкинуть
            obj.initials = Initials()
        for field in self.get_fields():
            if isinstance(field.widget, ManyToManyWidget):
                continue
            self.import_field(field, obj, data)

    def import_field(self, field, obj, data):
        if field.attribute and field.column_name in data:
            if field.attribute == 'collection':
                field.save(obj, data, sex=data.get(u'Пол'))
            elif field.attribute == 'tuck':
                obj.tuck = data[u'Вытачки'] != u'Без вытачки'
            elif field.attribute == 'clasp':
                obj.clasp = data[u'Застежка под штифты'] != u'Я не хочу использовать застежку под штифты'
            elif field.attribute in {'dickey__type', 'dickey__fabric'}:
                if data[u'Манишка'] != u'Я не хочу использовать манишку':
                    field.save(obj, data)
            elif field.attribute in {'initials__font', 'initials__color', 'initials__location'}:
                if data[u'Инициалы'] != u'Я не хочу использовать инициалы':
                    field.save(obj, data)
            else:
                field.save(obj, data)
        else:
            return None

    def get_diff(self, original, current, dry_run=False):
        data = []
        dmp = diff_match_patch()
        for field in self.get_fields():
            if field.attribute in {'tuck', 'stitch', 'clasp'}:
                v1 = getattr(original, 'get_%s_display' % field.attribute)() if original else '' # TODO: переименовать
                v2 = getattr(current, 'get_%s_display' % field.attribute)() if current else ''
            elif field.attribute in 'initials__location':
                v1 = original.initials.get_location_display() if original and original.initials is not None else ''
                v2 = current.initials.get_location_display() if current and current.initials is not None else ''
            else:
                v1 = self.export_field(field, original) if original else ""
                v2 = self.export_field(field, current) if current else ""
            diff = dmp.diff_main(force_text(v1), force_text(v2))
            dmp.diff_cleanupSemantic(diff)
            html = dmp.diff_prettyHtml(diff)
            html = mark_safe(html)
            data.append(html)
        return data


