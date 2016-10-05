# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0006_auto_20160919_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabriccolor',
            name='image_fabric',
            field=models.ImageField(upload_to=b'fabriccolor', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0434\u043b\u044f \u0444\u0438\u043b\u044c\u0442\u0440\u0430 \u0432\u043d\u0443\u0442\u0440\u0438 \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0442\u043e\u0440\u0430', blank=True),
        ),
        migrations.AddField(
            model_name='fabriccolor',
            name='image_filter',
            field=models.ImageField(upload_to=b'fabriccolor', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0434\u043b\u044f \u0444\u0438\u043b\u044c\u0442\u0440\u0430 \u043d\u0430 \u0432\u0438\u0442\u0440\u0438\u043d\u0435', blank=True),
        ),
    ]
