# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0074_auto_20160809_1825'),
        ('dictionaries', '0030_fit_sleevelength'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shirt',
            name='fit',
        ),
        migrations.RemoveField(
            model_name='shirt',
            name='sleeve_length',
        ),
        migrations.AddField(
            model_name='shirt',
            name='fit',
            field=models.ForeignKey(verbose_name='\u0422\u0430\u043b\u0438\u044f', blank=True, to='dictionaries.Fit', null=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='sleeve_length',
            field=models.ForeignKey(verbose_name='\u0414\u043b\u0438\u043d\u0430 \u0440\u0443\u043a\u0430\u0432\u0430', blank=True, to='dictionaries.SleeveLength', null=True),
        ),
    ]
