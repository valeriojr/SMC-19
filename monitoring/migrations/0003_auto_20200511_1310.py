# Generated by Django 3.0.4 on 2020-05-11 16:10

from django.db import migrations, models
import django.db.models.deletion
import validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('monitoring', '0002_auto_20200508_1651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionlog',
            name='model',
        ),
        migrations.AddField(
            model_name='actionlog',
            name='additional_info',
            field=models.TextField(default='', verbose_name='Informações adicionais'),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='object_id',
            field=models.PositiveIntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='address',
            name='neighbourhood',
            field=models.CharField(default='', max_length=100, verbose_name='Bairro'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cns',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[validators.validate_cns], verbose_name='Cartão do SUS'),
        ),
    ]
