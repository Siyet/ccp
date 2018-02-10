# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0020_auto_20171120_0929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customshirt',
            options={'verbose_name': '\u0421\u043e\u0440\u043e\u0447\u043a\u0430', 'verbose_name_plural': '\u0421\u043e\u0440\u043e\u0447\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='shirt',
            options={'ordering': ('code',), 'verbose_name': '\u0421\u043e\u0440\u043e\u0447\u043a\u0430', 'verbose_name_plural': '\u0421\u043e\u0440\u043e\u0447\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='standardshirt',
            options={'verbose_name': '\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0439 \u0432\u0430\u0440\u0438\u0430\u043d\u0442 \u0441\u043e\u0440\u043e\u0447\u043a\u0438', 'verbose_name_plural': '\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0435 \u0432\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0441\u043e\u0440\u043e\u0447\u0435\u043a'},
        ),
        migrations.AlterModelOptions(
            name='templateshirt',
            options={'verbose_name': '\u0428\u0430\u0431\u043b\u043e\u043d \u0441\u043e\u0440\u043e\u0447\u043a\u0438', 'verbose_name_plural': '\u0428\u0430\u0431\u043b\u043e\u043d\u044b \u0441\u043e\u0440\u043e\u0447\u0435\u043a'},
        ),
        migrations.RemoveField(
            model_name='collection',
            name='image',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='text',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='text_en',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='text_ru',
        ),
        migrations.RemoveField(
            model_name='shirt',
            name='sleeve_length',
        ),
        migrations.AlterField(
            model_name='collection',
            name='sex',
            field=models.CharField(default=b'male', max_length=6, verbose_name='\u041f\u043e\u043b \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f')]),
        ),
        migrations.AlterField(
            model_name='collection',
            name='sex_en',
            field=models.CharField(default=b'male', max_length=6, null=True, verbose_name='\u041f\u043e\u043b \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f')]),
        ),
        migrations.AlterField(
            model_name='collection',
            name='sex_ru',
            field=models.CharField(default=b'male', max_length=6, null=True, verbose_name='\u041f\u043e\u043b \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f')]),
        ),
        migrations.AlterField(
            model_name='contrastdetails',
            name='shirt',
            field=models.ForeignKey(related_name='contrast_details', verbose_name='\u0421\u043e\u0440\u043e\u0447\u043a\u0430', to='backend.Shirt'),
        ),
    ]
