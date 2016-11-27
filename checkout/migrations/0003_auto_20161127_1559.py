# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20160824_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdata',
            name='index',
            field=models.CharField(max_length=6, verbose_name='\u0418\u043d\u0434\u0435\u043a\u0441', blank=True),
        ),
        migrations.AlterField(
            model_name='customerdata',
            name='midname',
            field=models.CharField(max_length=255, verbose_name='\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e', blank=True),
        ),
    ]
