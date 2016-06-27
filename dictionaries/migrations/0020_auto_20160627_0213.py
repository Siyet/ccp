# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0019_auto_20160519_1940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ['sort_order'], 'verbose_name': '\u0412\u043e\u043f\u0440\u043e\u0441', 'verbose_name_plural': '\u0412\u043e\u043f\u0440\u043e\u0441\u044b \u0438 \u043e\u0442\u0432\u0435\u0442\u044b'},
        ),
        migrations.AddField(
            model_name='faq',
            name='sort_order',
            field=models.IntegerField(default=1, db_index=True, blank=True),
            preserve_default=False,
        ),
    ]
