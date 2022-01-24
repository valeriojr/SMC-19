from django.test import TestCase

from accounts.models import *
from monitoring.models import *


# Create your tests here.
from report import forms


# class ReportFormTest(TestCase):
#     def setUp(self):
#         self.group = Group.objects.create(name='group')
#         self.health_center = HealthCenter.objects.create(center_name='hge', group=self.group, active=True)
#         self.user = Account.objects.create(cpf='12345678909', first_name='João', last_name='Silva', group=self.group)
#         self.data = {
#             'report_type': 'monitoring',
#             'health_center': self.health_center,
#             'address_type': 'HM'
#         }
#
#     def test_minimum_input(self):
#         self.assertTrue(forms.StatusReportForm(data=self.data).is_valid())
#
#     def test_period(self):
#         period_data = {
#             'period_begin': '17/05/2020',
#             'period_end': '19/05/2020',
#         }
#
#         self.assertTrue(forms.StatusReportForm(data=dict(self.data, **period_data)).is_valid())
#
#         period_data = {
#             'period_begin': '15/05/2020',
#             'period_end': '14/05/2020',
#         }
#
#         self.assertFalse(forms.StatusReportForm(data=dict(self.data, **period_data)).is_valid())
#
#         period_data = {
#             'period_begin': '15/05/1400',
#         }
#
#         self.assertFalse(forms.StatusReportForm(data=dict(self.data, **period_data)).is_valid())
#
#         period_data = {
#             'period_end': '15/05/1400',
#         }
#
#         self.assertFalse(forms.StatusReportForm(data=dict(self.data, **period_data)).is_valid())
#
#         period_data = {
#             'period_begin': '15/05/2400',
#         }
#
#         self.assertFalse(forms.StatusReportForm(data=dict(self.data, **period_data)).is_valid())
#
#         period_data = {
#             'period_end': '15/05/2400',
#         }
#
#         self.assertFalse(forms.StatusReportForm(data=dict(self.data, **period_data)).is_valid())
#
#     def test_limit(self):
#         # Limite válido
#         print(forms.StatusReportForm(data=dict(self.data, limit=10)).errors)
#         self.assertTrue(forms.StatusReportForm(data=dict(self.data, limit=10)).is_valid())
#
#         # Limite inválido
#         self.assertFalse(forms.StatusReportForm(data=dict(self.data, limit=-5)).is_valid())
#
#         # Limite inválido
#         self.assertFalse(forms.StatusReportForm(data=dict(self.data, limit='a')).is_valid())
#
#         # Limite inválido
#         self.assertFalse(forms.StatusReportForm(data=dict(self.data, limit=1.5)).is_valid())
