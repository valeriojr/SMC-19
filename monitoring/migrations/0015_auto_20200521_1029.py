# Generated by Django 3.0.4 on 2020-05-21 13:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0014_auto_20200520_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoring',
            name='oxygen_saturation',
            field=models.FloatField(blank=True, default=0.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Saturação de oxigênio (%)'),
        ),
    ]