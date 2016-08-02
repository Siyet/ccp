# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0069_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirt',
            name='individualization',
            field=models.TextField(null=True, verbose_name='\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f', blank=True),
        ),
    ]
