from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.
import validators
from prediction.models import HealthCenter
from . import choices


class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, password=None):
        user = self.model(cpf=cpf)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, cpf, password=None):
        user = self.create_user(cpf=cpf, password=password)

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.first_login = False

        user.save(using=self._db)

        return user


class Group(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=50, default='')

    def __str__(self):
        return self.name


class Account(AbstractUser):

    class Meta:
        ordering = ['first_name', 'last_name']

    username = None
    first_name = models.CharField(verbose_name='Primeiro nome', max_length=100, default="")
    last_name = models.CharField(verbose_name='Sobrenome', max_length=100, default="")
    first_login = models.BooleanField(verbose_name='Primeiro Login', default=True)
    cpf = models.CharField(verbose_name='CPF', max_length=11, unique=True, validators=[validators.validate_cpf])
    user_profile = models.CharField(verbose_name='Tipo de usuário', max_length=2, choices=choices.user_profiles,
                                    default='AU')
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, blank=True, null=True)
    health_center = models.ForeignKey(HealthCenter, verbose_name='Unidade de Saúde', on_delete=models.SET_NULL,
                                      blank=True, null=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return "%s %s (CPF: %s)" % (self.first_name, self.last_name, self.cpf)
