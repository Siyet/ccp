# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('backend', '0067_auto_20160727_1521'),
        ('processing', '0029_yokeconfiguration'),
    ]

    operations = [
        migrations.CreateModel(
            name='StitchColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buttons_type', models.OneToOneField(verbose_name='\u041e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0430', to='backend.ElementStitch')),
                ('content_type', models.OneToOneField(verbose_name='\u0422\u0438\u043f \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u0435\u043a',
            },
        ),
        migrations.AlterField(
            model_name='collarmask',
            name='collar',
            field=models.ForeignKey(related_name='masks', to='processing.CollarConfiguration'),
        ),
        migrations.AlterField(
            model_name='cuffmask',
            name='cuff',
            field=models.ForeignKey(related_name='masks', to='processing.CuffConfiguration'),
        ),
    ]
