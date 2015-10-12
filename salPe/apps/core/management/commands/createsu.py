import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_model = get_user_model()
        if not user_model.objects.filter(username="admin").exists():
            password = os.environ['ADMIN_PASSWORD']
            user_model.objects.create_superuser("admin", "admin@admin.com", password)