# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20160910_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='contrast_details',
            field=models.BooleanField(default=True, verbose_name='\u041a\u043e\u043d\u0442\u0440\u0430\u0441\u0442\u043d\u044b\u0435 \u0434\u0435\u0442\u0430\u043b\u0438'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collection',
            name='white_fabric',
            field=models.ForeignKey(verbose_name='\u0422\u043a\u0430\u043d\u044c \u0434\u043b\u044f \u043e\u043f\u0446\u0438\u0438 "\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u0438 \u043c\u0430\u043d\u0436\u0435\u0442\u044b \u043f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e \u0431\u0435\u043b\u044b\u0435"', blank=True, to='backend.Fabric', null=True),
        ),
        migrations.AlterField(
            model_name='accessoriesprice',
            name='content_type',
            field=models.OneToOneField(related_name='accessories_price', verbose_name='content type', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='shirt',
            name='tuck',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'collections', to='dictionaries.TuckType', chained_field=b'collection', verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438'),
        ),
        migrations.AlterUniqueTogether(
            name='accessoriesprice',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='accessoriesprice',
            name='collections',
        ),
        migrations.RemoveField(
            model_name='accessoriesprice',
            name='object_pk',
        ),
    ]
