from django.test import TestCase
from django.utils import timezone

from accounts.models import Account, Group
from . import forms
from prediction.forms import HealthCenterForm

# Create your tests here.


class AccountTests(TestCase):

    def setUp(self):
        self.group = Group.objects.create(name='Test')
        self.health_center = HealthCenterForm(data={
            'center_name': 'SUS - Maceió',
            'latitude' : -9.66625,
            'longitude': -35.7351,
            'city': 'MACEIO',
            'state': 'AL',
            'active': True,
            'group': self.group,
        }).save()
        self.ss_user = Account(group=self.group, health_center=self.health_center, user_profile='SS')
        self.ad_user = Account(group=self.group, health_center=self.health_center, user_profile='AD')
        self.au_user = Account(group=self.group, health_center=self.health_center, user_profile='AU')

    def test_blacklisted_cpf(self):
        data = {
            'cpf': '11111111111',
            'user_profile': 'SS',
            'health_center': self.health_center,
            'password': 'qwcsczsc1',
            'confirm_password': 'qwcsczsc1'
        }

        form = forms.AccountCreationForm(data=data, user=self.ss_user)
        self.assertTrue(form.has_error('cpf'))

    def test_valid_cpf(self):

        data = {
            'cpf': '09716630417',
            'user_profile': 'SS',
            'health_center': self.health_center,
            'password': 'qwcsczsc1',
            'confirm_password': 'qwcsczsc1'
        }

        form = forms.AccountCreationForm(data=data, user=self.ss_user)
        self.assertTrue(not form.has_error('cpf'))

    def test_invalid_cpf(self):

        data = {
            'cpf': '12345678910',
        }

        form = forms.AccountCreationForm(data=data, user=self.ss_user)
        self.assertTrue(form.has_error('cpf'))

    def test_confirm_password_doesnt_match(self):

        data = {
            'first_name': 'Fulano',
            'last_name': 'Beltrano',
            'cpf': '00000000000',
            'user_profile': 'SS',
            'password': 'qwcsczsc1',
            'confirm_password': 'qwcsczsc'
        }

        form = forms.AccountCreationForm(data=data, user=self.ss_user)

        self.assertTrue(form.has_error('confirm_password'))

    def test_passwords_match(self):

        data = {
            'password': 'qwcsczsc1',
            'confirm_password': 'qwcsczsc1'
        }

        form = forms.AccountCreationForm(data=data, user=self.ss_user)
        self.assertTrue(not form.has_error('password') and not form.has_error('confirm_password'))

    def test_weak_password(self):
        data = {
            'first_name': 'Beltrano',
            'last_name': 'Fulano',
            'cpf': '00000000000',
            'user_profile': 'SS',
            'password': '12345678',
            'confirm_password': '12345678'
        }

        form = forms.AccountCreationForm(data=data, user=self.ss_user)

        self.assertFalse(not form.has_error('password') and not form.has_error('confirm_password'))