# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20161127_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='white_fabric',
            field=models.ForeignKey(related_name='white_set', verbose_name='\u0422\u043a\u0430\u043d\u044c \u0434\u043b\u044f \u043e\u043f\u0446\u0438\u0438 "\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u0438 \u043c\u0430\u043d\u0436\u0435\u0442\u044b \u043f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e \u0431\u0435\u043b\u044b\u0435"', blank=True, to='backend.Fabric', null=True),
        ),
    ]
