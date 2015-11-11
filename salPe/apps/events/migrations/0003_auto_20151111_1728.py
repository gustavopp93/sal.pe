# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151111_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtype',
            name='avatar',
        ),
        migrations.AddField(
            model_name='event',
            name='avatar',
            field=models.ImageField(upload_to='event/avatar', default=''),
            preserve_default=False,
        ),
    ]
