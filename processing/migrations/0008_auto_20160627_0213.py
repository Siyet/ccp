# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0007_auto_20160611_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='texture',
            name='texture',
            field=models.ImageField(upload_to=b'textures', verbose_name='\u0424\u0430\u0439\u043b \u0442\u0435\u043a\u0441\u0442\u0443\u0440\u044b'),
        ),
    ]
