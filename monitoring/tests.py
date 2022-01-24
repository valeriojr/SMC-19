import datetime

from django.contrib import messages
from django.shortcuts import render
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from accounts.forms import AccountCreationForm
from accounts.models import Account, Group
from monitoring.models import Profile, Address, ActionLog, Monitoring
from monitoring.views import ProfileDelete, ProfileCreate, MonitoringCreate
from prediction.forms import HealthCenterForm
from . import forms


# Create your tests here.


class ProfileFormTests(TestCase):

    def setUp(self):
        self.data = {
            'full_name': 'LA LI LU LE LO',
            'birth_date': timezone.now() - timezone.timedelta(days=1),
            'age': '23'
        }

    def test_full_name(self):
        # Nome vazio
        self.data['full_name'] = ''
        self.assertTrue(forms.ProfileForm(data=self.data).has_error('full_name'))

        # Nome válido
        self.data['full_name'] = 'Fulano da silva'
        self.assertFalse(forms.ProfileForm(data=self.data).has_error('full_name'))

    def test_age_assertion(self):
        self.data['age'] = -1
        self.assertTrue(forms.ProfileForm(data=self.data).has_error('age'))

        self.data['age'] = 'oi'
        self.assertTrue(forms.ProfileForm(data=self.data).has_error('age'))

        self.data['age'] = None
        self.assertTrue(forms.ProfileForm(data=self.data).has_error('age'))

    def test_birth_date_assertion(self):
        self.data['age'] = 1

        self.data['birth_date'] = timezone.now() + timezone.timedelta(weeks=1)
        self.assertFalse(forms.ProfileForm(data=self.data).is_valid())

        self.data['birth_date'] = timezone.now() + timezone.timedelta(days=1)
        self.assertFalse(forms.ProfileForm(data=self.data).is_valid())

        # Entre 0-2 horas a mais da data atual no futuro o form é válido
        self.data['birth_date'] = timezone.now() + timezone.timedelta(hours=3)
        self.assertFalse(forms.ProfileForm(data=self.data).is_valid())

    def test_phone(self):
        # Número de telefone válido
        self.data['phone_number'] = '82999823456'
        self.assertFalse(forms.ProfileForm(data=self.data).has_error('phone_number'))

        # Nùmero de telefone inválido
        self.data['phone_number'] = '82 99982-3456'
        self.assertTrue(forms.ProfileForm(data=self.data).has_error('phone_number'))

        self.data['phone_number'] = '5582999823456'
        self.assertTrue(forms.ProfileForm(data=self.data).has_error('phone_number'))

    def test_cpf(self):
        self.data['cpf'] = ''
        self.assertTrue(forms.ProfileForm(data=self.data).has_error('cpf'))

        self.data['cpf'] = '1234567909'
        self.assertTrue(forms.ProfileForm(data=self.data).has_error('cpf'))

        # A validação da unicidade do CPF foi movida do form para a view
        #
        # self.data['cpf'] = 'b2345678909'
        # self.assertTrue(forms.ProfileForm(data=self.data).has_error('cpf'))
        # # CPF repetido
        # self.data['cpf'] = '16526392091'
        # forms.ProfileForm(data=self.data).save()
        # self.assertTrue(forms.ProfileForm(data=self.data).has_error('cpf'))


class ProfileCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account.objects.create_user('12345678909', '12345678abc')

    def test_primary_address(self):
        form_data = {
            'full_name': 'Fulano da Silva',
            'birth_date': datetime.date(1999, 5, 17),
            'cpf': '82499631058',
            'age': 20,
            'address_set-TOTAL_FORMS': 1,
            'address_set-INITIAL_FORMS': 0,
            'address_set-0-city': 'MARAGOGI',
            'address_set-0-state': 'AL',
            'address_set-0-neighbourhood': 'Ademar Barbosa',
            'address_set-MAX_NUM_FORMS': '',
            'address_set-0-input_text_neighbourhood': 'Ademar Barbosa'
        }
        request = self.factory.post(reverse('monitoring:profile-create'), data=form_data)
        request._messages = messages.storage.default_storage(request)
        request.user = self.user

        response = ProfileCreate.as_view()(request)

        self.assertEquals(response.status_code, 302)
        profile = Profile.objects.all()[0]
        self.assertTrue(profile.address_set.all()[0].primary)


class ProfileDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account.objects.create_user('12345678909', '12345678abc')

        self.profile_to_delete = Profile.objects.create(full_name='Fulano da Silva', birth_date='1999-05-17',
                                                        cpf='82278572059')
        self.address = Address.objects.create(profile=self.profile_to_delete, city='MARAGOGI', state='AL',
                                              neighbourhood='ATEMAR DOS SANTOS')

    def test_delete_existent_profile(self):
        kwargs = {'pk': self.profile_to_delete.id}
        request = self.factory.post(reverse('monitoring:profile-delete', kwargs=kwargs))
        request.user = self.user

        response = ProfileDelete.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)  # Redireciona
        self.assertFalse(Profile.objects.filter(pk=self.profile_to_delete.id).exists())
        self.assertFalse(Profile.objects.filter(pk=self.address.id).exists())


class AddressFormTests(TestCase):

    def setUp(self):
        profile = forms.ProfileForm(data={
            'full_name': 'Fulano',
            'age': 1,
            'birth_date': timezone.now() - timezone.timedelta(days=10),
            'cpf': '41300642076'
        }).save()

        self.data = {
            'profile': profile,
        }


class MonitoringCreateFormTests(TestCase):

    def setUp(self):
        profile = forms.ProfileForm(data={
            'full_name': 'Fulano',
            'age': 1,
            'birth_date': timezone.now() - timezone.timedelta(days=10),
            'cpf': '32490624059',
        }).save()

        self.data = {
            'profile': profile,
            'attendance_date': timezone.now().date()
        }

    def test_results_assertion(self):
        self.data['result'] = 'Sr'
        self.assertFalse(forms.MonitoringForm(data=self.data).is_valid())

        self.data['result'] = -16
        self.assertFalse(forms.MonitoringForm(data=self.data).is_valid())

        self.data['result'] = 'SRR'
        self.assertFalse(forms.MonitoringForm(data=self.data).is_valid())

    def test_negative_referral_duration(self):
        self.data['medical_referral_duration'] = -14
        self.assertFalse(forms.MonitoringForm(data=self.data).is_valid())


class MonitoringCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account.objects.create_user('12345678909', '12345678abc')
        self.profile = Profile.objects.create(full_name='Fulano da Silva', cpf='27104119035')
        self.form_data = {
            'profile': self.profile.id,
            'result': 'SR',
            'created_by': self.user.id,
            'symptom_set-TOTAL_FORMS': 0,
            'symptom_set-INITIAL_FORMS': 0,
            'attendance_date': timezone.now().date()
        }

    def test_create_without_symptoms(self):
        request = self.factory.post(reverse('monitoring:monitoring-create'), data=self.form_data)
        request._messages = messages.storage.default_storage(request)
        request.user = self.user

        response = MonitoringCreate.as_view()(request)

        self.assertEquals(response.status_code, 302)
        monitoring = Monitoring.objects.latest('created')
        self.assertEquals(monitoring.score, 0)

    # def test_create_with_symptoms(self):
    #     data = dict(**self.form_data, **{
    #         'symptom_set-0-symptom': 'FV',
    #         'symptom_set-0-onset': timezone.now() - datetime.timedelta(days=2),
    #         'symptom_set-1-symptom': 'SB',
    #         'symptom_set-1-onset': timezone.now() - datetime.timedelta(days=5),
    #     })
    #     data['symptom_set-TOTAL_FORMS'] = 2
    #     data['symptom_set-INITIAL_FORMS'] = 0
    #     data['symptom_set-MAX_NUM_FORMS'] = 1000
    #
    #     print(data)
    #
    #     request = self.factory.post(reverse('monitoring:monitoring-create'), data=data)
    #     request._messages = messages.storage.default_storage(request)
    #     request.user = self.user
    #
    #     request.session = {}
    #     response = MonitoringCreate.as_view()(request)
    #
    #     self.assertEquals(response.status_code, 200)
    #     monitoring = Monitoring.objects.latest('created')
    #     self.assertEquals(monitoring.score, 15)


class SymptomCreateFormTests(TestCase):

    def setUp(self):
        profile = forms.ProfileForm(data={
            'full_name': 'Fulano',
            'age': 1,
            'birth_date': timezone.now() - timezone.timedelta(days=10),
            'cpf': '13280356032',
        }).save()

        monitoring_form = forms.MonitoringForm(data={
            'profile': profile,
            'result': 'SR',
            'attendance_date': timezone.now().date()
        })
        print(monitoring_form.errors)

        monitoring = monitoring_form.save()

        self.data = {
            'monitoring': monitoring,
            'symptom': 'CA',
            'type': 'TR',
            'intensity': 'L',
        }

    def test_future_onset(self):
        self.data['onset'] = timezone.now() + timezone.timedelta(days=1)
        self.assertFalse(forms.SymptomCreateForm(data=self.data).is_valid())


class TripCreateFormTests(TestCase):

    def setUp(self):
        profile = forms.ProfileForm(data={
            'full_name': 'Fulano',
            'age': 1,
            'birth_date': timezone.now() - timezone.timedelta(days=10),
            'cpf': '59890905019',
        }).save()

        self.data = {
            'profile': profile,
            'country': 'BRA'
        }

    def test_departure_after_return(self):
        self.data['departure_date'] = '01/01/1970'
        self.data['return_date'] = '31/12/1969'
        self.assertFalse(forms.TripForm(data=self.data).is_valid())

    def test_country_assertion(self):
        self.data['country'] = 'bRa'
        self.assertFalse(forms.TripForm(data=self.data).is_valid())

        self.data['country'] = None
        self.assertFalse(forms.TripForm(data=self.data).is_valid())

        self.data['country'] = 1
        self.assertFalse(forms.TripForm(data=self.data).is_valid())


class RequestCreateFormTests(TestCase):

    def setUp(self):
        c = Client()
        self.group = Group.objects.create(name='My Group')
        form = HealthCenterForm(data={
            'center_name': 'SUS - Maceió',
            'latitude': -9.66625,
            'longitude': -35.7351,
            'city': 'MACEIO',
            'state': 'AL',
            'active': True,
        })
        if not form.is_valid():
            print(form.errors)
        self.health_center = form.save()
        self.user = Account.objects.create(group=self.group, health_center=self.health_center)

        form = AccountCreationForm(data={
            'first_name': 'Fulano',
            'last_name': 'Beltrano',
            'cpf': "71161512063",
            'user_profile': 'SS',
            'password': 'qsczsewaxd',
            'confirm_password': ' qsczsewaxd',
            'health_center': self.health_center,
        }, user=self.user)

        if not form.is_valid():
            print(form.errors)
        user = form.save()

        c.force_login(user)

        unidade = HealthCenterForm(data={
            'center_name': "SUS-Maceió",
            'latitude': -9.1232434,
            'longitude': 35.456456,
            'active': True,
            'state': 'AL',
            'city': 'MACEIO'
        }).save()

        self.data = {
            'material': 'Seringa',
            'name': 'Jhonnye',
            'user': user,
            'unidade': unidade
        }

    def test_quantity_assertion(self):
        self.data['quantity'] = -1
        self.assertFalse(forms.RequestForm(data=self.data).is_valid())

        self.data['quantity'] = 'oi'
        self.assertFalse(forms.RequestForm(data=self.data).is_valid())

        self.data['quantity'] = None
        self.assertFalse(forms.RequestForm(data=self.data).is_valid())

    def test_unidade_assertion(self):
        self.data['quantity'] = 1
        self.data['unidade'] = None
        self.assertFalse(forms.RequestForm(data=self.data).is_valid())


class ActionLogCreateTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account.objects.create_user('1234567809', '12345678abc')
        self.profile = Profile.objects.create(full_name='Fulano', birth_date='1999-05-17', age=20, cpf='50636951081')

    # def test_create_monitoring_without_symptoms(self):
    #     request = self.factory.post(reverse('monitoring:monitoring-create'), data={
    #         'full_name': 'Fulano',
    #         'birth_date': '1999-05-17',
    #         'age': 20,
    #         'profile': self.profile.id,
    #         'result': 'NE',
    #         'symptom_set-INITIAL_FORMS': '0',
    #         'symptom_set-TOTAL_FORMS': '0',
    #         'symptom_set-MAX_NUM_FORMS': '',
    #     })
    #     request.user = self.user
    #     request._messages = messages.storage.default_storage(request)
    #
    #     response = MonitoringCreate.as_view()(request)
    #
    #     action_logs = ActionLog.objects.all()
    #     action_log = action_logs[0]
    #     monitoring = Monitoring.objects.all()[0]
    #
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEquals(action_logs.count(), 1)
    #     self.assertEquals(action_log.object_id, monitoring.id)
    #     self.assertEquals(action_log.action, 'C')


class ReportTest(TestCase):
    def setUp(self) -> None:
        pass
