# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0009_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buttonssource',
            name='ao',
            field=models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposingSource(b'%s/buttons/ao/%s'), null=True, verbose_name='\u0422\u0435\u043d\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='buttonssource',
            name='image',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/buttons/image/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='composesource',
            name='ao',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/ao/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0422\u0435\u043d\u0438'),
        ),
        migrations.AlterField(
            model_name='composesource',
            name='light',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/light/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0421\u0432\u0435\u0442'),
        ),
        migrations.AlterField(
            model_name='composesource',
            name='uv',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/uv/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='UV'),
        ),
        migrations.AlterField(
            model_name='texture',
            name='texture',
            field=models.ImageField(upload_to=b'textures', storage=processing.storage.OverwriteStorage(), verbose_name='\u0424\u0430\u0439\u043b \u0442\u0435\u043a\u0441\u0442\u0443\u0440\u044b'),
        ),
    ]
