from datetime import datetime

from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from django.forms.widgets import RadioSelect, Select
from accounts import choices
from . import models
import django.contrib.auth.password_validation as password_validation
from django.contrib.auth.hashers import make_password
from django.core import exceptions

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm


class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = models.Account
        exclude = ['last_login', 'user_permissions', 'is_active', 'is_staff', 'is_superuser', 'groups', 'date_joined']
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'password': forms.PasswordInput(),
            'user_profile': RadioSelect,
        }
        help_texts = {
            'first_name': 'Informe o primeiro nome do usuário.',
            'last_name': 'Informe o sobrenome do usuário.',
            'password': 'A senha deve ter no mínimo 8 caracteres.\nA senha não pode ser igual ao cpf.\nA senha não pode ser inteiramente númerica.\nA senha não pode ser muito comum.',
            'cpf': 'Apenas números',
            'user_profile': 'Escolha um item da lista'
        }

    confirm_password = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        super(AccountCreationForm, self).__init__(*args, **kwargs)
        if user.user_profile == 'SS':
            queryset = models.HealthCenter.objects.filter(group=user.group)
        else:
            queryset = models.HealthCenter.objects.filter(id=user.health_center.id)

        self.fields['health_center'].queryset = queryset.filter(active=True).order_by('center_name')

    def clean(self):
        cleaned_data = super(AccountCreationForm, self).clean()

        #checa se todas as chaves existem
        #cleaned_data só possuem os campos válidos.
        for key in ['first_name', 'last_name', 'password', 'confirm_password', 'health_center', 'user_profile']:
            if key not in cleaned_data:
                self.add_error(key, 'Campo deve ser preenchido')
                return cleaned_data
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        health_center = cleaned_data['health_center']
        user_profile = cleaned_data['user_profile']

        if password != confirm_password:
            self.add_error('confirm_password', 'As senhas não coincidem')
        if (user_profile == 'AU' or user_profile == 'AD') and (health_center is None):
            self.add_error('health_center', 'Você deve escolher uma unidade de saúde.')
        try:
            password_validation.validate_password(password, user=models.Account)
            cleaned_data['password'] = make_password(cleaned_data['password'])
            cleaned_data['confirm_password'] = cleaned_data['password']
        except exceptions.ValidationError as e:
            list_erros = list(e.messages)
            for error in list_erros:
                self.add_error('password', error)

        return cleaned_data


'''class PasswordChangeForm(PasswordChangeForm):
    def clean(self):
        old_password = self.cleaned_data["old_password"]
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        
        #print(old_password, new_password1)
        #print(old_password, new_password2)
        
        if old_password == new_password1 or old_password == new_password2:
            raise forms.ValidationError(
                message='A senha antiga não pode ser igual à atual.'
            )
        
        return self.cleaned_data'''
