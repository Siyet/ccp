# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0016_auto_20160630_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdata',
            name='email',
            field=models.EmailField(max_length=255, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
        ),
        migrations.AddField(
            model_name='order',
            name='certificate_value',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='\u041d\u043e\u043c\u0438\u043d\u0430\u043b \u0441\u0435\u0440\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u0430'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_value',
            field=models.FloatField(default=0, null=True, verbose_name='\u041d\u043e\u043c\u0438\u043d\u0430\u043b \u0441\u043a\u0438\u0434\u043a\u0438'),
        ),
    ]
