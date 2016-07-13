# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def move_source_links(apps, schema_editor):
    CuffButtonsSource = apps.get_model("processing", "CuffButtonsSource")

    def move_cuff(source):
        cuff = source.cuff_types.all().first()
        if not cuff:
            return False

        source.cuff = cuff
        return True

    def move_rounding(source):
        rounding = source.rounding
        if rounding:
            source.rounding_types.add(rounding)
        return True

    for source in CuffButtonsSource.objects.all():
        if move_cuff(source) and move_rounding(source):
            source.save()


class Migration(migrations.Migration):
    dependencies = [
        ('processing', '0019_auto_20160705_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuffbuttonssource',
            name='rounding_types',
            field=models.ManyToManyField(to='dictionaries.CuffRounding',
                                         verbose_name='\u0422\u0438\u043f\u044b \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f',
                                         blank=True),
        ),
        migrations.RunPython(move_source_links),
        migrations.AlterField(
            model_name='cuffbuttonssource',
            name='cuff',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f \u043c\u0430\u0436\u0435\u0442\u044b',
                                       to='dictionaries.CuffType'),
        ),
        migrations.RemoveField(
            model_name='cuffbuttonssource',
            name='cuff_types',
        ),
        migrations.RemoveField(
            model_name='cuffbuttonssource',
            name='rounding',
        ),
    ]
