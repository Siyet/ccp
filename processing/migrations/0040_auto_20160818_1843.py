# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0031_plackettype_show_buttons'),
        ('processing', '0039_initialsconfiguration_visible_with_pocket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='initialsconfiguration',
            name='visible_with_pocket',
        ),
        migrations.AddField(
            model_name='initialsconfiguration',
            name='pocket',
            field=models.ManyToManyField(to='dictionaries.PocketType', verbose_name='\u0412\u0438\u0434\u043d\u043e \u0441 \u043a\u0430\u0440\u043c\u0430\u043d\u043e\u043c'),
        ),
    ]
