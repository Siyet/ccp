# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0038_initialsconfiguration_initialsposition'),
    ]

    operations = [
        migrations.AddField(
            model_name='initialsconfiguration',
            name='visible_with_pocket',
            field=models.BooleanField(default=True, verbose_name='\u0412\u0438\u0434\u043d\u044b \u043f\u0440\u0438 \u043d\u0430\u043b\u0438\u0447\u0438\u0438 \u043a\u0430\u0440\u043c\u0430\u043d\u0430'),
        ),
    ]
