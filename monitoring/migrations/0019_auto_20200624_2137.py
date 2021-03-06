# Generated by Django 3.0.4 on 2020-06-25 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0018_auto_20200601_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='map_neighbours',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='Número de Vizinhos no Mapa'),
        ),
        migrations.AddField(
            model_name='profile',
            name='first_symptom_onset',
            field=models.DateField(blank=True, null=True, verbose_name='Data do primeiro sintoma'),
        ),
    ]
