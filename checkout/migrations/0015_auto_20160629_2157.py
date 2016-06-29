# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0014_auto_20160627_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='certificate',
            field=models.ForeignKey(blank=True, to='checkout.Certificate', null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='customer',
            field=models.OneToOneField(related_name='discount', primary_key=True, to_field=b'number', serialize=False, to='checkout.Customer', max_length=255, verbose_name='\u0423\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f'),
        ),
    ]
