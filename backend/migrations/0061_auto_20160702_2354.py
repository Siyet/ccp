# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0060_remove_cuff_sleeve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='image',
            field=models.ImageField(upload_to=b'collection', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='custombuttons',
            name='picture',
            field=models.ImageField(upload_to=b'custombuttons', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
    ]
