from django.core.management import BaseCommand

from monitoring.models import Monitoring
from django.db.models import F


class Command(BaseCommand):
    def handle(self, *args, **options):
        missing_attendance_date = Monitoring.objects.filter(attendance_date=None)
        missing_attendance_date.update(attendance_date=F('created'))
