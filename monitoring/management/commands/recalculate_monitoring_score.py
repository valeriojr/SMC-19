from django.core.management.base import BaseCommand

from monitoring import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        for monitoring in models.Monitoring.objects.all():
            monitoring.calculate_score()
            monitoring.save();
