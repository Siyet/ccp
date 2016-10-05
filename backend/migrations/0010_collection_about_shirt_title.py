# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20160919_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='about_shirt_title',
            field=models.CharField(default='', max_length=255, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u044d\u043a\u0440\u0430\u043d\u0430 "\u041e \u0441\u043e\u0440\u043e\u0447\u043a\u0435"'),
            preserve_default=False,
        ),
    ]
