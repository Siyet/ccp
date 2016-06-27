# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0012_auto_20160627_2051'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customerdata',
            unique_together=set([('order', 'type')]),
        ),
    ]
