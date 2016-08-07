# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0072_auto_20160807_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='filter_title',
            field=models.CharField(default="", max_length=255, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0444\u0438\u043b\u044c\u0442\u0440\u0430'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='material',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u041c\u0430\u0442\u0435\u0440\u0438\u0430\u043b', blank=True),
        ),
    ]
