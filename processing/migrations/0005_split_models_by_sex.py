# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def rebind_sources(apps, scheme_editor):
    ComposeSource = apps.get_model('processing', 'ComposeSource')
    ButtonsSource = apps.get_model('processing', 'ButtonsSource')
    CollarMask = apps.get_model('processing', 'CollarMask')
    StitchesSource = apps.get_model('processing', 'StitchesSource')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    def update_ct(model, old_name, new_name):
        try:
            objects = model.objects.filter(content_type__model=old_name)
        except:
            objects = model.objects.all()
        new_ct = ContentType.objects.get(app_label='male_configs', model=new_name)
        objects.update(content_type=new_ct)

    update_ct(ComposeSource, 'bodyconfiguration', 'malebodyconfiguration')
    update_ct(ComposeSource, 'backconfiguration', 'malebackconfiguration')
    update_ct(ComposeSource, 'collarconfiguration', 'malecollarconfiguration')
    update_ct(ComposeSource, 'placketconfiguration', 'maleplacketconfiguration')
    update_ct(ComposeSource, 'dickeyconfiguration', 'dickeyconfiguration')
    update_ct(ButtonsSource, 'collarbuttonsconfiguration', 'malecollarbuttonsconfiguration')
    update_ct(StitchesSource, 'collarbuttonsconfiguration', 'malecollarbuttonsconfiguration')

    CollarMask.objects.update(
        content_type_id=ContentType.objects.get(app_label='male_configs', model='malecollarconfiguration').id,
        object_id=models.F('collar_id')
    )


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('processing', '0004_rename_tables'),
        ('male_configs', '0001_initial')
    ]

    operations = [
        migrations.AddField(
            model_name='collarmask',
            name='content_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collarmask',
            name='object_id',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.RunPython(rebind_sources),
        migrations.AddField(
            model_name='bodybuttonsconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10,
                                   choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'),
                                            (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f'),
                                            (b'unisex', '\u0423\u043d\u0438\u0441\u0435\u043a\u0441')]),
        ),
        migrations.AddField(
            model_name='cuffbuttonsconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10,
                                   choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'),
                                            (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f'),
                                            (b'unisex', '\u0423\u043d\u0438\u0441\u0435\u043a\u0441')]),
        ),
        migrations.AddField(
            model_name='cuffconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10,
                                   choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'),
                                            (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f'),
                                            (b'unisex', '\u0423\u043d\u0438\u0441\u0435\u043a\u0441')]),
        ),
        migrations.AddField(
            model_name='initialsconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10,
                                   choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'),
                                            (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f'),
                                            (b'unisex', '\u0423\u043d\u0438\u0441\u0435\u043a\u0441')]),
        ),
        migrations.AddField(
            model_name='pocketconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10,
                                   choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'),
                                            (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f'),
                                            (b'unisex', '\u0423\u043d\u0438\u0441\u0435\u043a\u0441')]),
        ),
        migrations.AddField(
            model_name='yokeconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10,
                                   choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'),
                                            (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f'),
                                            (b'unisex', '\u0423\u043d\u0438\u0441\u0435\u043a\u0441')]),
        ),
        migrations.AlterField(
            model_name='bodybuttonsconfiguration',
            name='buttons',
            field=models.ForeignKey(verbose_name='\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b',
                                    to='dictionaries.CustomButtonsType'),
        ),
        migrations.AlterField(
            model_name='yokeconfiguration',
            name='yoke',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f \u043a\u043e\u043a\u0435\u0442\u043a\u0438',
                                    to='dictionaries.YokeType'),
        ),
        migrations.AlterUniqueTogether(
            name='bodybuttonsconfiguration',
            unique_together=set([('buttons', 'sex')]),
        ),
        migrations.AlterUniqueTogether(
            name='collarmask',
            unique_together=set([('object_id', 'content_type', 'element', 'projection')]),
        ),
        migrations.AlterUniqueTogether(
            name='yokeconfiguration',
            unique_together=set([('yoke', 'sex')]),
        ),
    ]
