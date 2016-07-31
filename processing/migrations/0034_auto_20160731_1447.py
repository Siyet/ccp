# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0033_auto_20160730_1625'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='texture',
            options={'ordering': ('texture',), 'verbose_name': '\u0422\u0435\u043a\u0441\u0442\u0443\u0440\u0430', 'verbose_name_plural': '\u0422\u0435\u043a\u0441\u0442\u0443\u0440\u044b'},
        ),
        migrations.AddField(
            model_name='texture',
            name='moire_filter',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0443\u0430\u0440 \u0444\u0438\u043b\u044c\u0442\u0440', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0412\u043a\u043b\u044e\u0447\u0435\u043d')]),
        ),
    ]
