# Generated by Django 3.0.4 on 2020-05-13 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0009_auto_20200513_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoring',
            name='blood_pressure',
            field=models.CharField(blank=True, default='', max_length=7, validators=[django.core.validators.RegexValidator('\\dx\\d', code='Erro', message='Informe a pressão arterial no formato. Ex.: 120x80 ou 12x8.')], verbose_name='Pressão arterial'),
        ),
    ]
