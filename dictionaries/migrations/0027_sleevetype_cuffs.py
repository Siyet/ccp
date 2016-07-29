# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0026_auto_20160702_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='sleevetype',
            name='cuffs',
            field=models.BooleanField(default=True, verbose_name='\u041c\u0430\u043d\u0436\u0435\u0442\u044b'),
        ),
    ]
