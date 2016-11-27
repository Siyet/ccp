# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0008_auto_20161108_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='backtype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='collarbuttons',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='collarbuttons',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='cuffrounding',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='cuffrounding',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='cufftype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='cufftype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='custombuttonstype',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='custombuttonstype',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='dickeytype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='dickeytype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='fabricdesign',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='fabricdesign',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='fabrictype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u0422\u0438\u043f'),
        ),
        migrations.AddField(
            model_name='fabrictype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u0422\u0438\u043f'),
        ),
        migrations.AddField(
            model_name='hemtype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='hemtype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='plackettype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='plackettype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='pockettype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='pockettype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='sizeoptions',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='sizeoptions',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='sleevelength',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='sleevelength',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='sleevetype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='sleevetype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='thickness',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='thickness',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='tucktype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='tucktype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='yoketype',
            name='title_en',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='yoketype',
            name='title_ru',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
