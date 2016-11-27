# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20161127_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='about_shirt_title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u044d\u043a\u0440\u0430\u043d\u0430 "\u041e \u0441\u043e\u0440\u043e\u0447\u043a\u0435"'),
        ),
        migrations.AddField(
            model_name='collection',
            name='about_shirt_title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u044d\u043a\u0440\u0430\u043d\u0430 "\u041e \u0441\u043e\u0440\u043e\u0447\u043a\u0435"'),
        ),
        migrations.AddField(
            model_name='collection',
            name='filter_title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0444\u0438\u043b\u044c\u0442\u0440\u0430'),
        ),
        migrations.AddField(
            model_name='collection',
            name='filter_title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0444\u0438\u043b\u044c\u0442\u0440\u0430'),
        ),
        migrations.AddField(
            model_name='collection',
            name='sex_en',
            field=models.CharField(default=b'male', max_length=6, null=True, verbose_name='\u041f\u043e\u043b \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f'), (b'unisex', '\u0423\u043d\u0438\u0441\u0435\u043a\u0441')]),
        ),
        migrations.AddField(
            model_name='collection',
            name='sex_ru',
            field=models.CharField(default=b'male', max_length=6, null=True, verbose_name='\u041f\u043e\u043b \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f'), (b'unisex', '\u0423\u043d\u0438\u0441\u0435\u043a\u0441')]),
        ),
        migrations.AddField(
            model_name='collection',
            name='tailoring_time_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043f\u043e\u0448\u0438\u0432\u0430 \u0438 \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u0438'),
        ),
        migrations.AddField(
            model_name='collection',
            name='tailoring_time_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043f\u043e\u0448\u0438\u0432\u0430 \u0438 \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u0438'),
        ),
        migrations.AddField(
            model_name='collection',
            name='text_en',
            field=models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='collection',
            name='text_ru',
            field=models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='collection',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='collection',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='custombuttons',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='custombuttons',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='elementstitch',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='elementstitch',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='fit',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='fit',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='hardness',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='hardness',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='shawloptions',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='shawloptions',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='stays',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='stays',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
