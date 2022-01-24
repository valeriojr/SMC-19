# Generated by Django 3.0.4 on 2020-05-15 00:15

import bitfield.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0011_auto_20200513_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoring',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data do atendimento'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='comorbidities',
            field=bitfield.models.BitField([('Y', 'Artrite reumatóide'), ('A', 'Asma'), ('C', 'Bronquite crônica'), ('N', 'Câncer'), ('E', 'Demência'), ('D', 'Diabetes'), ('H', 'Doença cardíacas'), ('L', 'Doença crônica no fígado'), ('R', 'Doença renal crônica'), ('W', 'Doenças reumáticas'), ('P', 'Doença pulmonar crônica'), ('I', 'Imunosuprimido'), ('T', 'Hipertensão'), ('V', 'HIV+'), ('B', 'Obesidade'), ('U', 'Portador de Lúpus')], blank=True, default=0, verbose_name='Comorbidades'),
        ),
    ]