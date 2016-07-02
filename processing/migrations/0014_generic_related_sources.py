# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.contenttypes.models import ContentType


def content_type_links_in_sources(apps, schema_editor):

    def migrate_sources(model, keys):
        for source in model.objects.all():
            for key in keys:
                fk = getattr(source, key, None)
                if not fk:
                    continue
                ct = ContentType.objects.get_for_model(fk._meta.model)
                source.content_type_id = ct.id
                source.object_id = fk.id
                source.save()
                break

    migrate_sources(
        apps.get_model("processing", "ComposeSource"),
        ['cuff_source', 'back_source', 'collar_source', 'body_source', 'placket_source', 'pocket_source']
    )

    migrate_sources(
        apps.get_model("processing", "ButtonsSource"),
        ['body_buttons', 'collar_buttons', 'cuff_buttons']
    )



class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0013_auto_20160702_1820'),
    ]

    operations = [
        migrations.RunPython(content_type_links_in_sources)
    ]
