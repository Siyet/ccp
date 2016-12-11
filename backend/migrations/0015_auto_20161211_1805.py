# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import backend.models
import dictionaries.models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_auto_20161210_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabric',
            name='long_description_en',
            field=models.TextField(default=b'', null=True, verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='long_description_ru',
            field=models.TextField(default=b'', null=True, verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='material_en',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name='\u041c\u0430\u0442\u0435\u0440\u0438\u0430\u043b', blank=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='material_ru',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name='\u041c\u0430\u0442\u0435\u0440\u0438\u0430\u043b', blank=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='short_description_en',
            field=models.TextField(default=b'', null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='short_description_ru',
            field=models.TextField(default=b'', null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='shirt',
            name='shawl',
            field=models.ForeignKey(related_name='shirts', default=dictionaries.models.ResolveDefault(backend.models.ShawlOptions), verbose_name='\u041f\u043b\u0430\u0442\u043e\u043a', to='backend.ShawlOptions', null=True),
        ),
    ]
