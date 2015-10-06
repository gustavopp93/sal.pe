# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.PositiveSmallIntegerField(default=0, choices=[(0, 'Inactivo'), (1, 'Activo'), (2, 'Eliminado')])),
                ('contact_phone', models.CharField(max_length=30)),
                ('contact_name', models.CharField(max_length=50)),
                ('contact_last_name', models.CharField(max_length=75)),
                ('contact_email', models.CharField(max_length=75)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('organization', models.ForeignKey(to='organizations.Organization')),
            ],
        ),
    ]
