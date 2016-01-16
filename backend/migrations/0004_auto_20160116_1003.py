# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_shirtimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='designs',
            field=models.ManyToManyField(related_name='design_fabrics', verbose_name='\u0414\u0438\u0437\u0430\u0439\u043d', to='dictionaries.FabricDesign'),
        ),
    ]
