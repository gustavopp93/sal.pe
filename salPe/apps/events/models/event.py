from django.db import models

from geoposition.fields import GeopositionField

from apps.organizations.models import Organization


class EventType(models.Model):
    name = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField()

    class Meta:
        app_label = 'events'


class Event(models.Model):
    event_type = models.ForeignKey(EventType)
    organization = models.ForeignKey(Organization)

    name = models.CharField(max_length=255)
    description = models.TextField()
    extra_data = models.TextField()

    position = GeopositionField()
    start_date = models.DateField()

    class Meta:
        app_label = 'events'
