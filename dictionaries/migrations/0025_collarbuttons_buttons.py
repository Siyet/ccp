# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0024_auto_20160629_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='collarbuttons',
            name='buttons',
            field=models.IntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0443\u0433\u043e\u0432\u0438\u0446', choices=[(0, 0), (1, 1), (2, 2)]),
        ),
    ]
