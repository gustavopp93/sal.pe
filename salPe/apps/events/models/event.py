from django.db import models

from geoposition.fields import GeopositionField

from apps.organizations.models import Organization


class EventType(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0

    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Activo', ),
        (STATUS_INACTIVE, 'Inactivo', )
    )

    name = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )

    def __str__(self):
        return self.name

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
