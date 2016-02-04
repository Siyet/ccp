# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0009_auto_20160204_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='collartype',
            name='image',
            field=models.ImageField(default=None, upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0434\u043b\u044f \u043f\u0440\u0435\u0432\u044c\u044e'),
            preserve_default=False,
        ),
    ]
