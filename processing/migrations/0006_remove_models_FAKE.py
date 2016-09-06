# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('processing', '0005_split_models_by_sex'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='backconfiguration',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='backconfiguration',
            name='back',
        ),
        migrations.RemoveField(
            model_name='backconfiguration',
            name='hem',
        ),
        migrations.RemoveField(
            model_name='backconfiguration',
            name='tuck',
        ),
        migrations.RemoveField(
            model_name='bodyconfiguration',
            name='cuff_types',
        ),
        migrations.RemoveField(
            model_name='bodyconfiguration',
            name='hem',
        ),
        migrations.RemoveField(
            model_name='bodyconfiguration',
            name='sleeve',
        ),
        migrations.AlterUniqueTogether(
            name='collarbuttonsconfiguration',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='collarbuttonsconfiguration',
            name='collar',
        ),
        migrations.AlterUniqueTogether(
            name='collarconfiguration',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='collarconfiguration',
            name='collar',
        ),
        migrations.AlterUniqueTogether(
            name='dickeyconfiguration',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='dickeyconfiguration',
            name='dickey',
        ),
        migrations.RemoveField(
            model_name='dickeyconfiguration',
            name='hem',
        ),
        migrations.RemoveField(
            model_name='placketconfiguration',
            name='hem',
        ),
        migrations.RemoveField(
            model_name='placketconfiguration',
            name='plackets',
        ),
        migrations.RemoveField(
            model_name='collarmask',
            name='collar',
        ),
        migrations.DeleteModel(
            name='BackConfiguration',
        ),
        migrations.DeleteModel(
            name='BodyConfiguration',
        ),
        migrations.DeleteModel(
            name='CollarButtonsConfiguration',
        ),
        migrations.DeleteModel(
            name='CollarConfiguration',
        ),
        migrations.DeleteModel(
            name='DickeyConfiguration',
        ),
        migrations.DeleteModel(
            name='PlacketConfiguration',
        ),
    ]
