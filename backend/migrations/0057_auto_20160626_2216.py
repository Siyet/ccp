# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0056_fabric_texture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ('order',), 'verbose_name': '\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u044f', 'verbose_name_plural': '\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438'},
        ),
        migrations.AlterModelOptions(
            name='custombuttons',
            options={'ordering': ('order',), 'verbose_name': '\u041a\u0430\u0441\u0442\u043e\u043c\u043d\u044b\u0435 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u044b', 'verbose_name_plural': '\u041a\u0430\u0441\u0442\u043e\u043c\u043d\u044b\u0435 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u044b'},
        ),
        migrations.AlterModelOptions(
            name='hardness',
            options={'ordering': ('order',), 'verbose_name': '\u0416\u0435\u0441\u0442\u043a\u043e\u0441\u0442\u044c', 'verbose_name_plural': '\u0416\u0435\u0441\u0442\u043a\u043e\u0441\u0442\u044c'},
        ),
        migrations.AlterModelOptions(
            name='shawloptions',
            options={'ordering': ('order',), 'verbose_name': '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043b\u0430\u0442\u043a\u0430', 'verbose_name_plural': '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043b\u0430\u0442\u043a\u0430'},
        ),
        migrations.AlterModelOptions(
            name='shirt',
            options={'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='stays',
            options={'ordering': ('order',), 'verbose_name': '\u041a\u043e\u0441\u0442\u043e\u0447\u043a\u0438', 'verbose_name_plural': '\u041a\u043e\u0441\u0442\u043e\u0447\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='templateshirt',
            options={'ordering': ('order',), 'verbose_name': '\u0428\u0430\u0431\u043b\u043e\u043d \u0440\u0443\u0431\u0430\u0448\u043a\u0438', 'verbose_name_plural': '\u0428\u0430\u0431\u043b\u043e\u043d\u044b \u0440\u0443\u0431\u0430\u0448\u0435\u043a'},
        ),
        migrations.AddField(
            model_name='collection',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='custombuttons',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hardness',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shawloptions',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shirt',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stays',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
    ]
