# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0004_delete_fit'),
        ('female_configs', '0003_femalebodysource'),
    ]

    operations = [
        migrations.CreateModel(
            name='FemaleBackShadow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('back', models.OneToOneField(verbose_name='\u0421\u043f\u0438\u043d\u043a\u0430', to='dictionaries.BackType')),
            ],
            options={
                'verbose_name': '\u0422\u0435\u043d\u044c \u0441\u043f\u0438\u043d\u043a\u0438',
                'verbose_name_plural': '\u0422\u0435\u043d\u0438 \u0441\u043f\u0438\u043d\u043a\u0438',
            },
        ),
    ]
