# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_auto_20161211_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='certificate',
            field=models.ForeignKey(verbose_name='\u0421\u0435\u0440\u0442\u0438\u0444\u0438\u043a\u0430\u0442', blank=True, to='checkout.Certificate', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(related_name='order', null=True, blank=True, to='checkout.Payment', verbose_name='\u041f\u043b\u0430\u0442\u0435\u0436'),
        ),
    ]
