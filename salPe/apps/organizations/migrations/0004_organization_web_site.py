# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_organization_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='web_site',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
