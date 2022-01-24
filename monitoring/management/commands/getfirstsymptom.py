from django.core.management import BaseCommand
from django.db.models import Min

from monitoring.models import Profile, Monitoring, Symptom


class Command(BaseCommand):
    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            try:
                profile.first_symptom_onset = Symptom.objects.filter(monitoring__profile=profile).earliest('onset').onset
                profile.save()
            except Symptom.DoesNotExist:
                pass