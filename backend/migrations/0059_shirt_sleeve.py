# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def copy_sleeve_from_cuff_to_shirts(apps, schema_editor):
    Shirt = apps.get_model("backend", "Shirt")
    for shirt in Shirt.objects.all():
        cuff = getattr(shirt, 'cuff', None)
        if cuff:
            shirt.sleeve = cuff.sleeve
            shirt.save()


class Migration(migrations.Migration):
    dependencies = [
        ('dictionaries', '0024_auto_20160629_1757'),
        ('backend', '0058_auto_20160628_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='shirt',
            name='sleeve',
            field=models.ForeignKey(related_name='sleeve_shirts', verbose_name='\u0420\u0443\u043a\u0430\u0432',
                                    to='dictionaries.SleeveType', null=True),
        ),
        migrations.RunPython(copy_sleeve_from_cuff_to_shirts)
    ]
