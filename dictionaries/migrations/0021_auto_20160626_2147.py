# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0020_sizeoptions_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collarbuttons',
            options={'ordering': ('order',), 'verbose_name': '\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430', 'verbose_name_plural': '\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430'},
        ),
        migrations.AlterModelOptions(
            name='cufftype',
            options={'ordering': ('order',), 'verbose_name': '\u0422\u0438\u043f \u043c\u0430\u043d\u0436\u0435\u0442\u044b', 'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442'},
        ),
        migrations.AlterModelOptions(
            name='fabricdesign',
            options={'ordering': ('order',), 'verbose_name': '\u041f\u0430\u0442\u0442\u0435\u0440\u043d \u0442\u043a\u0430\u043d\u0438', 'verbose_name_plural': '\u041f\u0430\u0442\u0442\u0435\u0440\u043d\u044b \u0442\u043a\u0430\u043d\u0435\u0439'},
        ),
        migrations.AlterModelOptions(
            name='fabrictype',
            options={'ordering': ('order',), 'verbose_name': '\u0422\u0438\u043f \u0442\u043a\u0430\u043d\u0438', 'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0442\u043a\u0430\u043d\u0435\u0439'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'ordering': ('order',), 'verbose_name': '\u0420\u0430\u0437\u043c\u0435\u0440 \u0440\u0443\u0431\u0430\u0448\u043a\u0438', 'verbose_name_plural': '\u0420\u0430\u0437\u043c\u0435\u0440\u044b \u0440\u0443\u0431\u0430\u0448\u0435\u043a'},
        ),
        migrations.AlterModelOptions(
            name='sizeoptions',
            options={'ordering': ('order',), 'verbose_name': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442 \u0440\u0430\u0437\u043c\u0435\u0440\u0430', 'verbose_name_plural': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0440\u0430\u0437\u043c\u0435\u0440\u043e\u0432'},
        ),
        migrations.AlterModelOptions(
            name='thickness',
            options={'ordering': ('order',), 'verbose_name': '\u0422\u043e\u043b\u0449\u0438\u043d\u0430 \u0442\u043a\u0430\u043d\u0438', 'verbose_name_plural': '\u0422\u043e\u043b\u0449\u0438\u043d\u0430 \u0442\u043a\u0430\u043d\u0438'},
        ),
        migrations.AddField(
            model_name='backtype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collarbuttons',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collartype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cufftype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dickeytype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fabricdesign',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fabrictype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hemtype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plackettype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pockettype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='size',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sleevetype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thickness',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yoketype',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
    ]
