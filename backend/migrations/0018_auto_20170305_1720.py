# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_auto_20161227_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='fit',
            name='picture_en',
            field=models.ImageField(upload_to=b'fit', null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='fit',
            name='picture_ru',
            field=models.ImageField(upload_to=b'fit', null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
    ]
