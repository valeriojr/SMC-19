# Generated by Django 3.0.4 on 2020-05-07 16:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('prediction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(default='', max_length=100, verbose_name='Primeiro nome')),
                ('last_name', models.CharField(default='', max_length=100, verbose_name='Sobrenome')),
                ('first_login', models.BooleanField(default=True, verbose_name='Primeiro Login')),
                ('cpf', models.CharField(max_length=11, unique=True, validators=[validators.validate_cpf], verbose_name='CPF')),
                ('user_profile', models.CharField(choices=[('AU', 'ATENDENTE DE UNIDADE'), ('AD', 'ADMINISTRADOR DE UNIDADE'), ('SS', 'SECRETARIA DE SAÚDE')], default='AU', max_length=2, verbose_name='Tipo de usuário')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('health_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prediction.HealthCenter', verbose_name='Unidade de Saúde')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]