# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0073_auto_20160807_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shirt',
            options={'ordering': ('code',), 'verbose_name': '\u0420\u0443\u0431\u0430\u0448\u043a\u0430', 'verbose_name_plural': '\u0420\u0443\u0431\u0430\u0448\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='templateshirt',
            options={'verbose_name': '\u0428\u0430\u0431\u043b\u043e\u043d \u0440\u0443\u0431\u0430\u0448\u043a\u0438', 'verbose_name_plural': '\u0428\u0430\u0431\u043b\u043e\u043d\u044b \u0440\u0443\u0431\u0430\u0448\u0435\u043a'},
        ),
        migrations.RemoveField(
            model_name='shirt',
            name='order',
        ),
        migrations.AlterField(
            model_name='collection',
            name='filter_title',
            field=models.CharField(max_length=255, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0444\u0438\u043b\u044c\u0442\u0440\u0430'),
        ),
    ]
