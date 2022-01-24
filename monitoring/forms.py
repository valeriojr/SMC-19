from datetime import datetime

from django import forms
from django.forms import inlineformset_factory
from pyUFbr.baseuf import ufbr

from monitoring import choices
from . import models

from prediction.models import HealthCenter


class MonitoringForm(forms.ModelForm):
    class Meta:
        model = models.Monitoring
        exclude = ('score',)
        labels = {
            'profile': 'Paciente'
        }
        widgets = {
            'profile': forms.widgets.Select,
            'collection_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'attendance_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'result_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'health_center': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),
            'status': forms.HiddenInput(),
        }
        help_texts = {
            'blood_pressure': 'Informe a pressão arterial no formato "MÁXIMOxMÍNIMO". Ex.: 120x80 ou 12x8.'
        }


class SymptomCreateForm(forms.ModelForm):
    class Meta:
        model = models.Symptom
        exclude = ['intensity']
        widgets = {
            'symptom': forms.HiddenInput(),
            'label': forms.HiddenInput(),
            'onset': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'intensity': forms.HiddenInput()
        }

    label = forms.CharField(widget=forms.HiddenInput(), required=False, empty_value='')


SymptomInlineFormset = inlineformset_factory(models.Monitoring, model=models.Symptom, form=SymptomCreateForm,
                                             extra=len(choices.symptom_choices), can_delete=False)


class TripForm(forms.ModelForm):
    class Meta:
        model = models.Trip
        fields = '__all__'
        widgets = {
            'profile': forms.HiddenInput(),
            'departure_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'return_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'state': forms.Select(choices=((uf, uf) for uf in ufbr.list_uf), attrs={'required': False}),
            'county': forms.Select()
        }

    def clean(self):
        cleaned_data = super(TripForm, self).clean()

        departure_date = cleaned_data['departure_date']
        return_date = cleaned_data['return_date']

        if departure_date is not None and return_date is not None and departure_date > return_date:
            self.add_error('departure_date', 'A data da ida não pode ser depois da volta')

        return cleaned_data


TripInlineFormset = inlineformset_factory(models.Profile, models.Trip, form=TripForm, extra=1)


class AddressForm(forms.ModelForm):
    
    field_order = ['state', 'city', 'neighbourhood', 'input_text_neighbourhood']
    input_text_neighbourhood = forms.CharField(label='Bairro', widget=forms.TextInput(), required=True, max_length=100)

    class Meta:
        model = models.Address
        exclude = ['primary', 'latitude', 'longitude', 'validated', 'map_neighbours']
        widgets = {
            'postal_code': forms.TextInput(attrs={'class': 'postal-code-field'}),
            'street_name': forms.TextInput(attrs={'class': 'street-name-field'}),
            'city': forms.Select(attrs={'class': 'city-field'}),
            'neighbourhood': forms.Select(attrs={'class': 'neighbourhood-field'}),
            'complement': forms.Textarea(attrs={'rows': 2}),
            'profile': forms.HiddenInput(),
        }
        labels = {
            'people': 'Número de pessoas residindo nesse endereço'
        }


AddressInlineFormset = inlineformset_factory(models.Profile, model=models.Address, extra=1, form=AddressForm,
                                             can_delete=False)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ['death_date', 'suspect_date', 'confirmed_date', 'discarded_date', 'recovered_date', 'monitored_date',
                   'group', 'first_monitoring', 'estimated_first_symptom']
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'family': forms.HiddenInput,
            'first_symptom_onset': forms.HiddenInput,
        }
        help_texts = {
            'phone_number': 'Apenas dígitos (0-9)',
            'cbo': 'Apenas para profissionais da saúde',
            'birthplace': 'Apenas para estrangeiros',
        }

    def clean_id_document(self):
        data = self.cleaned_data['id_document']

        for d in data:
            if d not in '0123456789':
                raise forms.ValidationError("Identidade só pode conter dígitos !")

        return data

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']

        if birth_date.year < 1900 or birth_date.year > datetime.now().date().year:
            raise forms.ValidationError('A data de nascimento não pode ser no futuro ou anterior a 1900!')

        return birth_date

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        cpf = cleaned_data.get('cpf')
        cns = cleaned_data.get('cns')
        birthplace = cleaned_data.get('birthplace')

        if not cpf:
            if cns and birthplace:
                self.add_error('cns',
                               'Informe o número de CNS apenas se o(a) paciente for brasileiro')
                self.add_error('birthplace',
                               'Informe o país de origem apenas se o(a) paciente for estrangeiro(a)')
                raise forms.ValidationError('Informações inválidas')
        if not cns:
            if cpf and birthplace:
                self.add_error('cpf',
                               'Informe o número de CPF se o(a) paciente for brasileiro')
                self.add_error('birthplace',
                               'Informe o país de origem do(a) paciente caso ele(a) seja estrangeiro(a)')
                raise forms.ValidationError('Informações inválidas')
        if not birthplace:
            if not(cpf or cns):
                self.add_error('cpf', 'Informe pelo menos o CPF ou CNS do(a) paciente')
                self.add_error('cns', 'Informe pelo menos o CPF ou CNS do(a) paciente')
                raise forms.ValidationError('Informações inválidas')

        if not (cpf or cns or birthplace):
            message = 'Informe pelo menos o CPF, CNS ou o país de origem do(a) paciente'
            self.add_error('cpf', message)
            self.add_error('cns', message)
            self.add_error('cns', message)
            raise forms.ValidationError('Informações inválidas')


class RequestForm(forms.ModelForm):
    class Meta:
        model = models.Request
        exclude = ['user']
        widgets = {
            'unidade': forms.widgets.Select,
        }


class SocialIsolationReportForm(forms.Form):
    reference_date = forms.DateField(label='Data de referência', required=False)
    medical_referral = forms.CharField(label='Tipo de encaminhamento', max_length=1, required=False, empty_value='',
                                       widget=forms.Select(choices=choices.medical_referral_choices))
    medical_referral_status = forms.CharField(label='Situação', max_length=1, required=False, empty_value='',
                                              widget=forms.Select(choices=choices.medical_referral_status_choices))


class MapForm(forms.Form):
    classification = forms.ChoiceField(label='Status', choices=(
        ('confirmado', 'Casos confirmados'),
        ('obito', 'Óbitos')
    ))


class HospitalizationForm(forms.ModelForm):
    class Meta:
        model = models.Hospitalization
        exclude = ('created', 'modified')
        labels = {
            'profile': 'Paciente',
            'healthcenter': 'Unidade de Saúde'
        }
        widgets = {
            'profile': forms.HiddenInput(),
            'healthcenter': forms.widgets.Select(),
            'bed_type': forms.Select(choices=choices.hospitalization_choices),
            'entry': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'departure': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean_health_center(self):
        health_center = self.cleaned_data['health_center']
        if health_center is None:
            raise forms.ValidationError('Unidade de saúde para internação não reconhecida')
        else:
            return health_center

    def clean_bed_type(self):
        bed_type = self.cleaned_data['bed_type']
        if bed_type not in [u[0] for u in choices.hospitalization_choices]:
            raise forms.ValidationError('Tipo de internação incorreto')
        else:
            return bed_type

    def clean(self):
        cleaned_data = super().clean()
        entry = cleaned_data.get('entry')
        departure = cleaned_data.get('departure')
        profile = cleaned_data.get('profile')
        hospitalizations = models.Hospitalization.objects.filter(profile=profile)

        if entry is None:
            raise forms.ValidationError('É obrigatório o preenchimento da data de entrada')
        else:
            if self.instance.id == None:
                if hospitalizations.filter(departure=None).count() != 0:
                    raise forms.ValidationError('Não é possivel internar o paciente quando ele está numa internação em andamento')
                elif hospitalizations.filter(departure__gt=entry).count() != 0:
                    raise forms.ValidationError('Não é possivel internar o paciente numa data de entrada antes de qualquer outra data de saída')
            else:
                if hospitalizations.filter(entry__gt=entry, departure__lt=entry).exclude(id=self.instance.id).count() != 0:
                    raise forms.ValidationError('Não é possível editar a data de entrada para uma data que intersecte outra internação')

        if departure is not None:
            if self.instance.id == None:
                print(departure)
                print(entry)
                if departure < entry:
                    raise forms.ValidationError('A data de saída não pode ser antes da data de entrada')
            else:
                if hospitalizations.filter(entry__gt=departure, departure__lt=departure).exclude(id=self.instance.id).count() != 0:
                    raise forms.ValidationError('Não é possível editar a data de saída para uma data que intersecte outra internação')

        return cleaned_data


class ContactForm(forms.ModelForm):
    phone_number = forms.CharField(label='Telefone', max_length=15, min_length=14, widget=forms.TextInput(attrs={
                'type': 'tel',
                'placeholder': "(XX) XXXXX-XXXX",
            }))
    class Meta:
        model = models.Contact
        exclude = ('created',)
        widgets = {
            'profile': forms.HiddenInput(),
            'contact_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        phone_number = ''.join(c for c in phone_number if c.isdigit())

        if len(phone_number) not in [10, 11]:
            raise forms.ValidationError('É necessário 10 dígitos para número de telefone fixo ou 11 para número de celular (incluindo o DDD)')

        return phone_number

class VaccinationForm(forms.ModelForm):
    class Meta:
        model = models.Vaccination
        fields = '__all__'
        labels = {
            'profile': 'Paciente',
        }
        widgets = {
            'profile': forms.HiddenInput(),
            'dose': forms.widgets.Select(),
            'vaccine': forms.widgets.Select(),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }