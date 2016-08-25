# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(related_name='items', verbose_name='\u0417\u0430\u043a\u0430\u0437', to='checkout.Order'),
        ),
        migrations.AlterModelTable(
            name='orderitem',
            table='checkout_orderdetails',
        ),
    ]
