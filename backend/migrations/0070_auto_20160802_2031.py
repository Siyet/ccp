# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0069_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirt',
            name='individualization',
            field=models.TextField(null=True, verbose_name='\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f', blank=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='fit',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u0422\u0430\u043b\u0438\u044f', choices=[(b'classic', '\u041a\u043b\u0430\u0441\u0441\u0438\u0447\u0435\u0441\u043a\u0430\u044f'), (b'fitted', '\u041f\u0440\u0438\u0442\u0430\u043b\u0435\u043d\u043d\u0430\u044f'), (b'very_fitted', '\u041e\u0447\u0435\u043d\u044c \u043f\u0440\u0438\u0442\u0430\u043b\u0435\u043d\u043d\u0430\u044f')]),
        ),
        migrations.AddField(
            model_name='shirt',
            name='sleeve_length',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u0414\u043b\u0438\u043d\u0430 \u0440\u0443\u043a\u0430\u0432\u0430', choices=[(b'normal', '\u041e\u0431\u044b\u0447\u043d\u044b\u0439'), (b'long', '\u0414\u043b\u0438\u043d\u043d\u044b\u0439'), (b'shorter', '\u0423\u043a\u043e\u0440\u043e\u0447\u0435\u043d\u043d\u044b\u0439')]),
        ),
    ]
