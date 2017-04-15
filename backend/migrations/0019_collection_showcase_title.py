# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_auto_20170305_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='showcase_title',
            field=models.CharField(default='', max_length=255, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0432\u0438\u0442\u0440\u0438\u043d\u044b'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collection',
            name='showcase_title_en',
            field=models.CharField(max_length=255, null=True,
                                   verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0432\u0438\u0442\u0440\u0438\u043d\u044b'),
        ),
        migrations.AddField(
            model_name='collection',
            name='showcase_title_ru',
            field=models.CharField(max_length=255, null=True,
                                   verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0432\u0438\u0442\u0440\u0438\u043d\u044b'),
        )
    ]
