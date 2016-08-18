# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from backend.models import Initials


def remove_initials(apps, scheme_editor):
    Initials.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0076_custombuttons_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shirt',
            name='initials',
        ),
        migrations.RunPython(remove_initials),
        migrations.AddField(
            model_name='initials',
            name='shirt',
            field=models.OneToOneField(related_name='initials', to='backend.Shirt'),
            preserve_default=False,
        ),
    ]
