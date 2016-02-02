# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0006_auto_20160202_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('size', models.PositiveIntegerField(unique=True, serialize=False, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440', primary_key=True)),
            ],
            options={
                'verbose_name': '\u0420\u0430\u0437\u043c\u0435\u0440 \u0440\u0443\u0431\u0430\u0448\u043a\u0438',
                'verbose_name_plural': '\u0420\u0430\u0437\u043c\u0435\u0440\u044b \u0440\u0443\u0431\u0430\u0448\u0435\u043a',
            },
        ),
        migrations.CreateModel(
            name='SizeOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('show_options', models.BooleanField(default=True, verbose_name='\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u0440\u0430\u0437\u043c\u0435\u0440\u044b')),
            ],
            options={
                'verbose_name': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442 \u0440\u0430\u0437\u043c\u0435\u0440\u0430',
                'verbose_name_plural': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0440\u0430\u0437\u043c\u0435\u0440\u043e\u0432',
            },
        ),
    ]
