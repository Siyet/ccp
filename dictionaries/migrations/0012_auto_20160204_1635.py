# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0011_cufftype_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u0441\u043f\u0438\u043d\u043a\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0441\u043f\u0438\u043d\u043e\u043a',
            },
        ),
        migrations.CreateModel(
            name='HemType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043d\u0438\u0437\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043d\u0438\u0437\u0430',
            },
        ),
        migrations.CreateModel(
            name='PlacketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043f\u043e\u043b\u043e\u0447\u043a\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043f\u043e\u043b\u043e\u0447\u0435\u043a',
            },
        ),
        migrations.CreateModel(
            name='PocketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043a\u0430\u0440\u043c\u0430\u043d\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043a\u0430\u0440\u043c\u0430\u043d\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='SleeveType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u0440\u0443\u043a\u0430\u0432\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0440\u0443\u043a\u0430\u0432\u043e\u0432',
            },
        ),
        migrations.RemoveField(
            model_name='collartype',
            name='image',
        ),
        migrations.RemoveField(
            model_name='cufftype',
            name='image',
        ),
        migrations.AddField(
            model_name='collartype',
            name='picture',
            field=models.ImageField(default=None, upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cufftype',
            name='picture',
            field=models.ImageField(default=None, upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fabricdesign',
            name='title',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='yoketype',
            name='title',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
