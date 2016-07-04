# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0026_auto_20160702_2354'),
        ('processing', '0016_auto_20160702_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuffmasksource',
            name='cuff',
        ),
        migrations.AddField(
            model_name='bodysource',
            name='cuff_types',
            field=models.ManyToManyField(related_name='body_sources', verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442', to='dictionaries.CuffType'),
        ),
        migrations.AddField(
            model_name='cuffbuttonssource',
            name='cuff_types',
            field=models.ManyToManyField(related_name='cuff_button_sources', verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442', to='dictionaries.CuffType'),
        ),
        migrations.AddField(
            model_name='cuffsource',
            name='cuff_types',
            field=models.ManyToManyField(related_name='cuff_sources', verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442', to='dictionaries.CuffType'),
        ),
        migrations.AddField(
            model_name='cuffsource',
            name='side_mask',
            field=models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposingSource(b'composesource/%s/%s'), null=True, verbose_name='\u041c\u0430\u0441\u043a\u0430 \u0440\u0443\u043a\u0430\u0432\u0430 (\u0441\u0431\u043e\u043a\u0443)'),
        ),
        migrations.AlterField(
            model_name='cuffmask',
            name='cuff',
            field=models.ForeignKey(to='processing.CuffSource'),
        ),
        migrations.DeleteModel(
            name='CuffMaskSource',
        ),
    ]
