from django.conf import settings
from django.db import models


class Organization(models.Model):

    STATUS_INACTIVE = 0
    STATUS_ACTIVE = 1
    STATUS_DELETED = 2

    STATUS_CHOICES = (
        (STATUS_INACTIVE, 'Inactivo', ),
        (STATUS_ACTIVE, 'Activo'),
        (STATUS_DELETED, 'Eliminado'),
    )

    name = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=STATUS_INACTIVE)

    avatar = models.ImageField(upload_to=settings.ORGANIZATION_AVATAR_DIR)
    web_site = models.URLField()

    contact_phone = models.CharField(max_length=30)
    contact_name = models.CharField(max_length=50)
    contact_last_name = models.CharField(max_length=75)
    contact_email = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'organizations'


class OrganizationUser(models.Model):

    organization = models.ForeignKey(Organization)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        app_label = 'organizations'
