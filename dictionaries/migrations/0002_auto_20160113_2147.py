# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collartype',
            name='title',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='cuffrounding',
            name='title',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='cufftype',
            name='title',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='dickeytype',
            name='title',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
