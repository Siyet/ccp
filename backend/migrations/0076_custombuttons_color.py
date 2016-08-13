# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0075_auto_20160811_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='custombuttons',
            name='color',
            field=colorful.fields.RGBColorField(default=b'#FFFFFF', verbose_name='\u0426\u0432\u0435\u0442'),
        ),
    ]
