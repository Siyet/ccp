# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def move_source_links(apps, schema_editor):
    PlacketConfiguration = apps.get_model("processing", "PlacketConfiguration")

    for conf in PlacketConfiguration.objects.all():
        placket = conf.placket
        if placket:
            conf.plackets.add(placket)
        conf.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0031_plackettype_show_buttons'),
        ('processing', '0036_auto_20160811_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='placketconfiguration',
            name='plackets',
            field=models.ManyToManyField(to='dictionaries.PlacketType', verbose_name='\u0422\u0438\u043f \u043f\u043e\u043b\u043e\u0447\u043a\u0438'),
        ),
        migrations.RunPython(move_source_links),
        migrations.AlterUniqueTogether(
            name='placketconfiguration',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='placketconfiguration',
            name='placket',
        ),
    ]
