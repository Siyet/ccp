# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('processing', '0012_auto_20160702_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollarMask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection', models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f', choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('mask', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'composesource/%s/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0424\u0430\u0439\u043b \u043c\u0430\u0441\u043a\u0438')),
            ],
            options={
                'verbose_name': '\u041c\u0430\u0441\u043a\u0430 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u041c\u0430\u0441\u043a\u0438 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
            },
        ),
        migrations.AddField(
            model_name='collarsource',
            name='buttons',
            field=models.IntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0443\u0433\u043e\u0432\u0438\u0446', choices=[(0, 0), (1, 1), (2, 2)]),
        ),
        migrations.AddField(
            model_name='composesource',
            name='content_type',
            field=models.ForeignKey(default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='composesource',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buttonssource',
            name='content_type',
            field=models.ForeignKey(default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buttonssource',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collarsource',
            name='collar',
            field=models.ForeignKey(verbose_name='\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a', to='dictionaries.CollarType'),
        ),
        migrations.AlterUniqueTogether(
            name='collarsource',
            unique_together=set([('collar', 'buttons')]),
        ),
        migrations.AddField(
            model_name='collarmask',
            name='collar',
            field=models.ForeignKey(to='processing.CollarSource'),
        ),
    ]
