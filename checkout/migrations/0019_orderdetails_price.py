# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.transaction import atomic


def set_prices(apps, scheme_editor):
    OrderDetails = apps.get_model('checkout', 'OrderDetails')
    for x in OrderDetails.objects.select_related('shirt'):
        x.price = x.shirt.price
        x.save()


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0018_order_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='price',
            field=models.DecimalField(verbose_name='\u0426\u0435\u043d\u0430', null=True, editable=False, max_digits=10, decimal_places=2),
        ),
        migrations.RunPython(set_prices),
    ]
