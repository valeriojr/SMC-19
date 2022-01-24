# Generated by Django 3.0.4 on 2020-05-27 14:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitoring', '0015_auto_20200521_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='latitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='address',
            name='longitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='Longitude'),
        ),
        migrations.AddField(
            model_name='address',
            name='validated',
            field=models.BooleanField(blank=True, default=False, verbose_name='Endereço Validado'),
        ),
        migrations.AddField(
            model_name='monitoring',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Criado por'),
        ),
        migrations.AddField(
            model_name='profile',
            name='ethnicity',
            field=models.CharField(blank=True, choices=[('A', 'Amarela'), ('B', 'Branca'), ('I', 'Indígena'), ('P', 'Parda'), ('p', 'Preta')], default='', max_length=1, verbose_name='Etnia'),
        ),
        migrations.AddField(
            model_name='profile',
            name='profession',
            field=models.CharField(blank=True, choices=[('', 'Nenhuma')], default='', max_length=5, verbose_name='Profissão'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cpf',
            field=models.CharField(default='', max_length=11, validators=[validators.only_digits, validators.validate_cpf], verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='request',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantidade necessária'),
        ),
    ]
