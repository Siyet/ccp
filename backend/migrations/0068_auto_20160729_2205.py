# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0067_auto_20160727_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirt',
            name='is_template',
            field=models.BooleanField(default=False, verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442\u0441\u044f \u043a\u0430\u043a \u0448\u0430\u0431\u043b\u043e\u043d'),
        ),
    ]
