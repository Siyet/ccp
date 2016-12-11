# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0009_auto_20161127_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabriccolor',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='fabriccolor',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
