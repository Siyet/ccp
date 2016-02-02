# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0004_fabriccategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShirtInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('text', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043f\u043e\u0434 \u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u043e\u043c')),
            ],
        ),
        migrations.CreateModel(
            name='ShirtInfoImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name='\u0424\u0430\u0439\u043b')),
                ('text', models.ImageField(upload_to=b'', verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043f\u043e\u0434 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435\u043c')),
                ('shirt_info', models.ForeignKey(related_name='images', to='dictionaries.ShirtInfo')),
            ],
            options={
                'verbose_name': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f',
            },
        ),
    ]
