# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20160116_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='image',
            field=models.ImageField(default=None, upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collection',
            name='text',
            field=models.TextField(default='', verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
            preserve_default=False,
        ),
    ]
