# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CollarButtons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
            },
        ),
        migrations.CreateModel(
            name='CollarType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('buttons', models.ManyToManyField(to='dictionaries.CollarButtons', verbose_name='\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u043f\u0443\u0433\u043e\u0432\u0438\u0446')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', colorful.fields.RGBColorField(verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0426\u0432\u0435\u0442 (\u0434\u043b\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432)',
                'verbose_name_plural': '\u0426\u0432\u0435\u0442\u0430 (\u0434\u043b\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432)',
            },
        ),
        migrations.CreateModel(
            name='CuffRounding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f \u043c\u0430\u043d\u0436\u0435\u0442\u044b',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f \u043c\u0430\u043d\u0436\u0435\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='CuffType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('rounding', models.ManyToManyField(to='dictionaries.CuffRounding', verbose_name='\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043c\u0430\u043d\u0436\u0435\u0442\u044b',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442',
            },
        ),
        migrations.CreateModel(
            name='CustomButtonsType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('extra_price', models.DecimalField(verbose_name='\u0414\u043e\u0431\u0430\u0432\u043e\u0447\u043d\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c', max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
            },
        ),
        migrations.CreateModel(
            name='DickeyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043c\u0430\u043d\u0438\u0448\u043a\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0438\u0448\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='FabricColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('value', colorful.fields.RGBColorField(verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0426\u0432\u0435\u0442 \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u0426\u0432\u0435\u0442\u0430 \u0442\u043a\u0430\u043d\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='FabricDesign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u041f\u0430\u0442\u0442\u0435\u0440\u043d \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u041f\u0430\u0442\u0442\u0435\u0440\u043d\u044b \u0442\u043a\u0430\u043d\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='StitchColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('color', colorful.fields.RGBColorField(verbose_name='\u0426\u0432\u0435\u0442')),
            ],
            options={
                'verbose_name': '\u0426\u0432\u0435\u0442 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438',
                'verbose_name_plural': '\u0426\u0432\u0435\u0442\u0430 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='YokeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043a\u043e\u043a\u0435\u0442\u043a\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043a\u043e\u043a\u0435\u0442\u043a\u0438',
            },
        ),
    ]
