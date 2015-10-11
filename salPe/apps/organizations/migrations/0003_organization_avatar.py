# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organizationuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='avatar',
            field=models.ImageField(upload_to='organization/avatar', default=''),
            preserve_default=False,
        ),
    ]
