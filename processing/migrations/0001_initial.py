# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-05 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComposingSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(b'EXR', 'UV (\u0432 \u0444\u043e\u0440\u043c\u0430\u0442\u0435 EXR)'), (b'LIGHT', '\u0421\u0432\u0435\u0442 (png)'), (b'SHADOW', '\u0422\u0435\u043d\u044c (png)'), (b'TEXTURE', '\u0422\u0435\u043a\u0441\u0442\u0443\u0440\u0430')], max_length=10, verbose_name='\u0422\u0438\u043f')),
                ('file', models.FileField(upload_to=b'sources', verbose_name='\u0424\u0430\u0439\u043b')),
            ],
            options={
                'verbose_name': '\u0418\u0441\u0445\u043e\u0434\u043d\u0438\u043a',
                'verbose_name_plural': '\u0418\u0441\u0445\u043e\u0434\u043d\u0438\u043a\u0438 \u0434\u043b\u044f \u043a\u043e\u043c\u043f\u043e\u0437\u0430',
            },
        ),
    ]
