# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0025_collarbuttons_buttons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backtype',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='collartype',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='cufftype',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='dickeytype',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='fabricdesign',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='hemtype',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='plackettype',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='pockettype',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='shirtinfoimage',
            name='image',
            field=models.ImageField(upload_to=b'shirtinfo', verbose_name='\u0424\u0430\u0439\u043b'),
        ),
        migrations.AlterField(
            model_name='sleevetype',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='yoketype',
            name='picture',
            field=models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
    ]
