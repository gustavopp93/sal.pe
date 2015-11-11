# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtype',
            name='avatar',
            field=models.ImageField(default='', upload_to='event/avatar'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, 'Activo'), (0, 'Inactivo')]),
        ),
    ]
