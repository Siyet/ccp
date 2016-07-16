# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path
from django.contrib.contenttypes.models import ContentType


def rename_content_types(apps, schema_editor):
    rename_operations = filter(lambda op: isinstance(op, migrations.RenameModel), Migration.operations)
    for rename in rename_operations:
        ct = ContentType.objects.get(model=rename.old_name.lower())
        ct.model = rename.new_name.lower()
        ct.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0026_auto_20160702_2354'),
        ('processing', '0022_merge'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BodyButtonsSource',
            new_name='BodyButtonsConfiguration',
        ),
        migrations.RenameModel(
            old_name='CollarSource',
            new_name='CollarConfiguration',
        ),
        migrations.RenameModel(
            old_name='CollarButtonsSource',
            new_name='CollarButtonsConfiguration',
        ),
        migrations.RenameModel(
            old_name='CuffButtonsSource',
            new_name='CuffButtonsConfiguration',
        ),
        migrations.RenameModel(
            old_name='PlacketSource',
            new_name='PlacketConfiguration',
        ),
        migrations.RenameModel(
            old_name='PocketSource',
            new_name='PocketConfiguration',
        ),
        migrations.RenameModel(
            old_name='BackSource',
            new_name='BackConfiguration',
        ),
        migrations.RenameModel(
            old_name='BodySource',
            new_name='BodyConfiguration',
        ),
        migrations.RenameModel(
            old_name='CuffSource',
            new_name='CuffConfiguration',
        ),
        migrations.AlterField(
            model_name='buttonssourcecache',
            name='source',
            field=models.ForeignKey(related_name='cache', to='processing.ButtonsSource'),
        ),
        migrations.RunPython(rename_content_types)
    ]
