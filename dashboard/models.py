from django.db import models

# Create your models here.
from accounts.models import Group
from monitoring.models import Profile


class EpidemiologicalReport(models.Model):
    confirmed = models.PositiveIntegerField(verbose_name='Casos confirmados', default=0)
    suspect = models.PositiveIntegerField(verbose_name='Casos suspeitos', default=0)
    recovered = models.PositiveIntegerField(verbose_name='Recuperados', default=0)
    deaths = models.PositiveIntegerField(verbose_name='Óbitos confirmados', default=0)
    discarded = models.PositiveIntegerField(verbose_name='Descartados', default=0)
    monitored = models.PositiveIntegerField(verbose_name='Monitorados', default=0)

    date = models.DateField(verbose_name='Data', unique_for_date=True, null=True)
    group = models.ForeignKey(verbose_name='Grupo', to=Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'Informe epidemiológico ({self.date.strftime("%d/%m/%Y")})'
