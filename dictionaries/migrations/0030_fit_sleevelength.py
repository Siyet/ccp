# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0029_auto_20160807_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0422\u0438\u043f \u0442\u0430\u043b\u0438\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0442\u0430\u043b\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='SleeveLength',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0422\u0438\u043f \u0434\u043b\u0438\u043d\u044b \u0440\u0443\u043a\u0430\u0432\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0434\u043b\u0438\u043d\u044b \u0440\u0443\u043a\u0430\u0432\u0430',
            },
        ),
    ]
