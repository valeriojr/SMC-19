# Generated by Django 3.0.4 on 2020-06-26 15:38

from django.db import migrations, models
import validators


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0020_auto_20200625_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='death_date',
            field=models.DateField(default=None, null=True, validators=[validators.prevent_future_date, validators.only_after_2020], verbose_name='Data do óbito'),
        ),
    ]
