# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.models.configuration
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0025_collarbuttons_buttons'),
        ('processing', '0015_auto_20160702_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuffMask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection', models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f', choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('mask', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'composesource/%s/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0424\u0430\u0439\u043b \u043c\u0430\u0441\u043a\u0438')),
                ('element', models.CharField(max_length=20, verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442', choices=[(b'cuff_outer', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 \u0432\u043d\u0435\u0448\u043d\u044f\u044f'), (b'cuff_inner', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f')])),
            ],
            options={
                'verbose_name': '\u041c\u0430\u0441\u043a\u0430 \u043c\u0430\u043d\u0436\u0435\u0442\u044b',
                'verbose_name_plural': '\u041c\u0430\u0441\u043a\u0438 \u043c\u0430\u043d\u0436\u0435\u0442',
            },
        ),
        migrations.CreateModel(
            name='CuffMaskSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dickey_mask', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'composesource/%s/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u041c\u0430\u0441\u043a\u0430 \u043c\u0430\u043d\u0438\u0448\u043a\u0438')),
                ('cuff', models.OneToOneField(verbose_name='\u0422\u0438\u043f \u043c\u0430\u043d\u0436\u0435\u0442\u044b', to='dictionaries.CuffType')),
            ],
            options={
                'verbose_name': '\u041c\u0430\u0441\u043a\u0438 \u043c\u0430\u043d\u0436\u0435\u0442\u044b',
                'verbose_name_plural': '\u041c\u0430\u0441\u043a\u0438 \u043c\u0430\u043d\u0436\u0435\u0442',
            },
        ),
        migrations.RemoveField(
            model_name='buttonssourcecache',
            name='bounding_box',
        ),
        migrations.RemoveField(
            model_name='composesourcecache',
            name='bounding_box',
        ),
        migrations.AddField(
            model_name='buttonssourcecache',
            name='pos_repr',
            field=models.CommaSeparatedIntegerField(default='(0, 0)', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collarmask',
            name='element',
            field=models.CharField(default='collar_face', max_length=20, verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442', choices=[(b'collar_face', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u043b\u0438\u0446\u0435\u0432\u0430\u044f \u0441\u0442\u043e\u0440\u043e\u043d\u0430'), (b'collar_bottom', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u043d\u0438\u0437'), (b'collar_outer', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u0432\u043d\u0435\u0448\u043d\u044f\u044f \u0441\u0442\u043e\u0439\u043a\u0430'), (b'collar_inner', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f \u0441\u0442\u043e\u0439\u043a\u0430')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='composesourcecache',
            name='pos_repr',
            field=models.CommaSeparatedIntegerField(default='(0, 0)', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collarbuttonssource',
            name='buttons',
            field=models.IntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0443\u0433\u043e\u0432\u0438\u0446', choices=[(0, 0), (1, 1), (2, 2)]),
        ),
        migrations.AlterUniqueTogether(
            name='buttonssource',
            unique_together=set([('content_type', 'object_id', 'projection')]),
        ),
        migrations.AlterUniqueTogether(
            name='collarmask',
            unique_together=set([('collar', 'element', 'projection')]),
        ),
        migrations.AlterUniqueTogether(
            name='composesource',
            unique_together=set([('content_type', 'object_id', 'projection')]),
        ),
        migrations.AddField(
            model_name='cuffmask',
            name='cuff',
            field=models.ForeignKey(to='processing.CuffMaskSource'),
        ),
        migrations.AlterUniqueTogether(
            name='cuffmask',
            unique_together=set([('cuff', 'element', 'projection')]),
        ),
    ]
