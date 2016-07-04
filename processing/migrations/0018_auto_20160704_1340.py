# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def move_cuff_links(apps, schema_editor):
    def move_cuffs(model):
        for source in model.objects.all():
            cuff = source.cuff
            if not cuff:
                continue

            source.cuff_types.add(cuff)
            source.save()

    move_cuffs(apps.get_model("processing", "BodySource"))
    move_cuffs(apps.get_model("processing", "CuffSource"))
    move_cuffs(apps.get_model("processing", "CuffButtonsSource"))


class Migration(migrations.Migration):
    dependencies = [
        ('processing', '0017_auto_20160704_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodysource',
            name='cuff_types',
            field=models.ManyToManyField(to='dictionaries.CuffType',
                                         verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442'),
        ),
        migrations.AlterField(
            model_name='cuffsource',
            name='cuff_types',
            field=models.ManyToManyField(to='dictionaries.CuffType',
                                         verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442'),
        ),
        migrations.AlterField(
            model_name='cuffbuttonssource',
            name='cuff_types',
            field=models.ManyToManyField(to='dictionaries.CuffType',
                                         verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442'),
        ),
        migrations.AlterUniqueTogether(
            name='bodysource',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='cuffbuttonssource',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='cuffsource',
            unique_together=set([]),
        ),
        migrations.RunPython(move_cuff_links),
        migrations.RemoveField(
            model_name='bodysource',
            name='cuff',
        ),
        migrations.RemoveField(
            model_name='cuffbuttonssource',
            name='cuff',
        ),
        migrations.RemoveField(
            model_name='cuffsource',
            name='cuff',
        ),
    ]
