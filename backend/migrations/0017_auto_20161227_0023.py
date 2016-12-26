# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20161213_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='code',
            field=models.CharField(unique=True, max_length=20, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b', validators=[django.core.validators.RegexValidator(b'[A-Z]+\\d+', message='\u041d\u0435\u0434\u043e\u043f\u0443\u0441\u0442\u0438\u043c\u044b\u0439 \u043a\u043e\u0434 \u0441\u043e\u0440\u043e\u0447\u043a\u0438: \u043c\u043e\u0436\u0435\u0442 \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u0442\u044c \u0442\u043e\u043b\u044c\u043a\u043e \u043b\u0430\u0442\u0438\u043d\u0441\u043a\u0438\u0435 \u0441\u0438\u043c\u0432\u043e\u043b\u044b \u0438 \u0446\u0438\u0444\u0440\u044b')]),
        ),
    ]
