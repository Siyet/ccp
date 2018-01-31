# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_auto_20180131_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='image',
        ),
        migrations.AddField(
            model_name='collection',
            name='text',
            field=models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
    ]
