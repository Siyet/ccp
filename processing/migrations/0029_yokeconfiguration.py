# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0026_auto_20160702_2354'),
        ('processing', '0028_auto_20160724_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='YokeConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yoke', models.OneToOneField(verbose_name='\u0422\u0438\u043f \u043a\u043e\u043a\u0435\u0442\u043a\u0438', to='dictionaries.YokeType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u043e\u043a\u0435\u0442\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u043e\u043a\u0435\u0442\u043a\u0438',
            },
        ),
    ]
