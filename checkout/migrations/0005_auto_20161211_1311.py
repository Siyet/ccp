# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20161127_1610'),
    ]

    operations = [
        migrations.DeleteModel(name='OrderItem'),
        migrations.DeleteModel(name='CustomerData'),
        migrations.DeleteModel(name='Order')
    ]
