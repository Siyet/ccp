# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def remove_dickeys(apps, scheme_editor):
    Dickey = apps.get_model('backend', 'Dickey')
    Dickey.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0062_auto_20160707_1306'),
    ]

    operations = [
        migrations.RunPython(remove_dickeys),
        migrations.AlterModelOptions(
            name='customshirt',
            options={},
        ),
        migrations.AlterModelOptions(
            name='shirt',
            options={'verbose_name': '\u0420\u0443\u0431\u0430\u0448\u043a\u0430', 'verbose_name_plural': '\u0420\u0443\u0431\u0430\u0448\u043a\u0438'},
        ),
        migrations.RemoveField(
            model_name='shirt',
            name='dickey',
        ),
        migrations.AddField(
            model_name='dickey',
            name='shirt',
            field=models.ForeignKey(related_name='dickey', default=None, to='backend.Shirt'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contrastdetails',
            name='shirt',
            field=models.ForeignKey(related_name='contrast_details', verbose_name='\u0420\u0443\u0431\u0430\u0448\u043a\u0430', to='backend.Shirt'),
        ),
    ]
