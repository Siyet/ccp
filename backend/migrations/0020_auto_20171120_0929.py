# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_collection_showcase_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirt',
            name='stitch',
            field=models.CharField(max_length=10, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438', choices=[(b'none', '0 \u043c\u043c (\u0431\u0435\u0437 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438)'), (b'1mm', '1 \u043c\u043c (\u0442\u043e\u043b\u044c\u043a\u043e \u0441\u043e \u0441\u044a\u0435\u043c\u043d\u044b\u043c\u0438 \u043a\u043e\u0441\u0442\u043e\u0447\u043a\u0430\u043c\u0438)'), (b'5mm', '5 \u043c\u043c')]),
        ),
    ]
