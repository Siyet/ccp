# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0017_auto_20160703_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(default=b'new', max_length=20, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(b'new', '\u041e\u0436\u0438\u0434\u0430\u0435\u0442 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438'), (b'completed', '\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u043d')]),
        ),
        migrations.AddField(
            model_name='order',
            name='date_add',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f', null=True),
        ),
    ]
