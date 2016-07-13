# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.models.configuration


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0026_auto_20160702_2354'),
        ('processing', '0020_auto_20160705_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='DickeyConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dickey', models.ForeignKey(verbose_name='\u0422\u0438\u043f \u043c\u0430\u043d\u0438\u0448\u043a\u0438', to='dictionaries.DickeyType')),
                ('hem', models.ForeignKey(verbose_name='\u041d\u0438\u0437', blank=True, to='dictionaries.HemType', null=True)),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043c\u0430\u043d\u0438\u0448\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043c\u0430\u043d\u0438\u0448\u043a\u0438',
            },
            bases=(models.Model, processing.models.configuration.SourceMixin),
        ),
        migrations.AlterUniqueTogether(
            name='dickeyconfiguration',
            unique_together=set([('dickey', 'hem')]),
        ),
    ]
