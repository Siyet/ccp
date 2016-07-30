# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0067_auto_20160727_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='texture',
            field=models.OneToOneField(related_name='fabric', null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0422\u0435\u043a\u0441\u0442\u0443\u0440\u0430', to='processing.Texture'),
        ),
    ]
