# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_organization_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('extra_data', models.TextField()),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
                ('start_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(to='events.EventType'),
        ),
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(to='organizations.Organization'),
        ),
    ]
