from datetime import timedelta

from bitfield import BitField
from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.db.models import When, Case, Value, IntegerField, Q, F
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from pyUFbr.baseuf import ufbr

import validators
from accounts.models import Account, Group
from geolocation.models import Geolocator, validate_city
from prediction.models import HealthCenter
from smc19.settings import GOOGLE_API_KEY
from . import choices


# Create your models here.

class Profile(models.Model):
    class Meta:
        ordering = ['-id']

    full_name = models.CharField(verbose_name='Nome completo', max_length=100)
    mother_name = models.CharField(verbose_name='Nome da mãe', max_length=100, blank=True, default='')
    birth_date = models.DateField(verbose_name='Data de nascimento',
                                  validators=[validators.prevent_past_date, validators.prevent_future_date], null=True)
    cns = models.CharField(verbose_name='Cartão do SUS', max_length=15, blank=True,
                           validators=[validators.validate_cns], null=True)
    id_document = models.CharField(verbose_name='RG', max_length=15, blank=True, default='000000000')
    cbo = models.CharField(verbose_name='CBO', max_length=7, blank=True, default='')
    cpf = models.CharField(verbose_name='CPF', max_length=11, blank=True, default='',
                           validators=[validators.only_digits, validators.validate_cpf])
    birthplace = models.CharField(verbose_name='País de origem', max_length=30, blank=True, default='')
    passport = models.CharField(verbose_name='Passaporte', max_length=16, blank=True, default='')
    phone_number = models.CharField(verbose_name='Número de telefone', max_length=12,
                                    validators=[validators.only_digits], blank=True, default='')
    gender = models.CharField(verbose_name='Sexo biológico', max_length=1, choices=choices.gender_choices, blank=True,
                              default='')
    age = models.PositiveIntegerField(verbose_name='Idade', default=0)
    weight = models.FloatField(verbose_name='Peso (Kg)', blank=True, default=0,
                               validators=[MinValueValidator(0)])
    height = models.FloatField(verbose_name='Altura (m)', blank=True, default=0, validators=[MinValueValidator(0)])
    ethnicity = models.CharField(verbose_name='Etnia', max_length=1, choices=choices.ethnicity_choices, blank=True,
                                 default='')
    profession = models.CharField(verbose_name='Profissão', max_length=30, blank=True, default='')
    security_professional = models.BooleanField(verbose_name='Profissional de segurança', default=False)
    smoker = models.BooleanField(verbose_name='Fumante', blank=True, default=False)
    vaccinated = models.BooleanField(verbose_name='Tomou vacina da gripe em 2020', blank=True, default=False)
    oxygen = models.BooleanField(verbose_name='Precisou de oxigênio recentemente', blank=True, default=False)
    comorbidities = BitField(verbose_name='Comorbidades', flags=choices.comorbidity_choices, blank=True, default=0)
    family = models.ForeignKey(to='Family', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    first_symptom_onset = models.DateField(verbose_name='Data do primeiro sintoma', blank=True, null=True)
    suspect_date = models.DateField(verbose_name='Data que virou suspeito',
                                    validators=[validators.prevent_future_date, validators.only_after_2020],
                                    null=True, default=None)
    confirmed_date = models.DateField(verbose_name='Data de confirmação',
                                      validators=[validators.prevent_future_date, validators.only_after_2020],
                                      null=True, default=None)
    death_date = models.DateField(verbose_name='Data do óbito',
                                  validators=[validators.prevent_future_date, validators.only_after_2020],
                                  null=True, default=None)
    monitored_date = models.DateField(verbose_name='Data do fim do monitoramento',
                                      validators=[validators.prevent_future_date, validators.only_after_2020],
                                      null=True, default=None)
    discarded_date = models.DateField(verbose_name='Data de descarte',
                                      validators=[validators.prevent_future_date, validators.only_after_2020],
                                      null=True, default=None)
    recovered_date = models.DateField(verbose_name='Data de recuperação',
                                      validators=[validators.prevent_future_date, validators.only_after_2020],
                                      null=True, default=None)
    group = models.ForeignKey(verbose_name='Grupo', to=Group, on_delete=models.SET_NULL, null=True)
    estimated_first_symptom = models.DateField(verbose_name='Data estimada do primeiro sintoma',
                                               validators=[validators.prevent_future_date, validators.only_after_2020],
                                               null=True, blank=True)

    def make_familiar(self, other):
        if self.family is None:
            if other.family is None:
                family = Family.objects.create()

                Profile.objects.filter(id__in=[self.id, other.id]).update(family=family)
            else:
                Profile.objects.filter(id=self.id).update(family=other.family)
        else:
            if other.family is None:
                Profile.objects.filter(id=other.id).update(family=self.family)
            else:
                Profile.objects.filter(family=other.family).update(family=self.family)

    @staticmethod
    def get_status(date):
        """
        Retorna a contagem geral de cada caso num dia dado.
        Para a contagem diária, use a função count_daily() do dashboard.utils
        """
        return {
            'confirmed': Case(When(confirmed_date__lte=date, then=Value(1, output_field=IntegerField())),
                              default=Value(0)),
            'suspect': Case(When(death_date__isnull=True, suspect_date__lte=date, discarded_date__gt=date,
                                 confirmed_date__isnull=True, then=Value(1, output_field=IntegerField())),
                            default=Value(0)),
            'dead': Case(When(death_date__lte=date, then=Value(1, output_field=IntegerField())),
                         default=Value(0)),
            'monitored': Case(
                When(death_date__isnull=True, monitored_date__gte=date, then=Value(1, output_field=IntegerField())),
                default=Value(0)),
            'discarded': Case(
                When(death_date__isnull=True, discarded_date__lte=date, recovered_date__isnull=True,
                     then=Value(1, output_field=IntegerField())), default=Value(0)),
            'recovered': Case(
                When((Q(death_date__isnull=True) | Q(recovered_date__lt=F('death_date'))) & Q(recovered_date__lte=date),
                     then=Value(1, output_field=IntegerField())),
                default=Value(0)),
        }

    def fill_first_symptoms_date(self):
        first_symptom = Symptom.objects.filter(monitoring__profile=self).order_by('onset').first()
        if first_symptom is not None:
            assert first_symptom.onset is not None, \
                "Sintoma sem data! (id=%d, monitoring=%d)" % (self.id, first_symptom.monitoring.id)
            self.first_symptom_onset = first_symptom.onset
            self.estimated_first_symptom = None

    def fill_estimated_first_symptoms_date(self, displacement):
        """
        Define a data do primeiro atendimento utilizando o deslocamento dado.

        displacement: Média das diferenças entre data do primeiro sintoma e do
        atendimento. Calculado na função mean_diff_attendance_symptom() do
        monitoring.utils.
        """
        first_monitoring = Monitoring.objects.filter(profile=self).order_by('attendance_date').first()
        if first_monitoring is not None and self.first_symptom_onset is None:
            assert first_monitoring.attendance_date is not None, \
                "Atendimento sem data! (id=%d, monitoring=%d)" % (self.id, first_monitoring.id)
            self.estimated_first_symptom = first_monitoring.attendance_date - timedelta(days=displacement)

    def is_confirmed(self):
        return self.confirmed_date is not None

    def is_suspect(self):
        return self.suspect_date is not None

    def has_first_symptom(self):
        return self.first_symptom_onset is not None

    def __str__(self):
        return f'{self.full_name}'


class Address(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    primary = models.BooleanField(verbose_name='Principal', blank=True, default=False)
    type = models.CharField(verbose_name='Tipo', max_length=2, choices=choices.address_type_choices, blank=True,
                            default='')
    postal_code = models.CharField(verbose_name='CEP', max_length=8, blank=True, default='')
    neighbourhood = models.CharField(verbose_name='Bairro', max_length=100, default='')
    street_name = models.CharField(verbose_name='Logradouro', max_length=100, blank=True, default='')
    number = models.PositiveIntegerField(verbose_name='Número', blank=True, null=True, default=0)
    complement = models.CharField(verbose_name='Complemento', max_length=100, blank=True, default='')
    city = models.CharField(verbose_name='Cidade', max_length=30, blank=False)
    state = models.CharField(verbose_name='Estado', max_length=2, choices=zip(ufbr.list_uf, ufbr.list_uf), blank=False)
    people = models.PositiveIntegerField(verbose_name='Quantidade de pessoas', blank=True, null=True, default=1)

    latitude = models.FloatField(
        verbose_name='Latitude',
        validators=[MinValueValidator(-90), MaxValueValidator(+90)],
        blank=True, null=True
    )
    longitude = models.FloatField(
        verbose_name='Longitude',
        validators=[MinValueValidator(-180), MaxValueValidator(+180)],
        blank=True, null=True
    )
    validated = models.BooleanField(verbose_name='Endereço Validado', blank=True, default=False)
    map_neighbours = models.PositiveIntegerField(verbose_name='Número de Vizinhos no Mapa', blank=True, default=1)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.profile.address_set.count() == 0:
            self.primary = True

        if self.latitude is None and self.longitude is None:
            geolocator = Geolocator(api_key=GOOGLE_API_KEY)
            geolocator_result = geolocator.geocode(address=str(self))

            geolocation_config = apps.get_app_config('geolocation')
            validators = geolocation_config.validators
            current_validator = validators[self.city] if self.city in validators.keys() else None

            if geolocator_result is not None:

                self.latitude, self.longitude = geolocator_result['location']['lat'], geolocator_result['location'][
                    'lng']

                if not validate_city(self.city, geolocator_result['city']):
                    self.validated = False
                else:
                    if current_validator is not None:
                        if current_validator.validate_polygon(self.neighbourhood, self.latitude, self.longitude):
                            self.validated = True
                        elif current_validator.validate_knn(self.neighbourhood, self.latitude, self.longitude):
                            self.validated = True
                        else:
                            self.validated = False
                    else:
                        self.validated = True

        return super(Address, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.primary:
            for address in self.profile.address_set.exclude(id=self.id).order_by('type'):
                address.primary = True
                address.save()
                break

        super(Address, self).delete(using, keep_parents)

    def __str__(self):
        return '%s, %s, %s, %s, %s - %s, %s' % (
            self.street_name, str(self.number or 'S/N'), self.complement, self.neighbourhood, self.city,
            self.state, self.postal_code)


class Monitoring(models.Model):
    class Meta:
        ordering = ['-created']

    profile = models.ForeignKey(Profile, models.CASCADE)
    status = models.CharField(verbose_name='Status', max_length=1, choices=choices.status_choices, blank=True)
    virus_exposure = BitField(verbose_name='Exposição COVID-19', flags=choices.exposure_choices, blank=True, default=0)
    # Sinais vitais
    oxygen_saturation = models.FloatField(verbose_name='Saturação de oxigênio (%)',
                                          validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True,
                                          default=0.0)
    temperature = models.FloatField(verbose_name='Temperatura', blank=True, null=True,
                                    validators=[MinValueValidator(35.0), MaxValueValidator(45.0)])
    pulse = models.PositiveIntegerField(verbose_name='Pulso', blank=True, null=True)
    blood_pressure = models.CharField(verbose_name='Pressão arterial', max_length=7, blank=True, default='',
                                      validators=[RegexValidator('\dx\d', code='Erro',
                                                                 message='Informe a pressão arterial no formato "MÁXIMOxMÍNIMO". Ex.: 120x80 ou 12x8.')])
    result = models.CharField(verbose_name='Resultado do exame', max_length=2, choices=choices.result_choices,
                              default='SR')
    created = models.DateTimeField(verbose_name='Data de inclusão', auto_now_add=True)
    professional = models.CharField(verbose_name='Nome do profissional', max_length=50, blank=True, default='')
    attendance_date = models.DateField(verbose_name='Data de atendimento',
                                       validators=[validators.prevent_future_date, validators.only_after_2020],
                                       null=True)
    health_center = models.ForeignKey(verbose_name='Unidade de saúde', to=HealthCenter, on_delete=models.SET_NULL,
                                      blank=True, null=True)
    created_by = models.ForeignKey(verbose_name='Criado por', to=Account, on_delete=models.SET_NULL, blank=True,
                                   null=True)
    # Formulário de Maragogi
    community_health_agent_name = models.CharField(max_length=100, verbose_name='Nome do agente comunitário de saúde',
                                                   blank=True, default='')
    hypothesis = models.TextField(verbose_name='Hipótese diagnóstica', blank=True, default='')
    tests = models.CharField(verbose_name='Exames solicitados para COVID-19', max_length=2,
                             choices=choices.tests_choices, blank=True, default='N')
    collection_date = models.DateField(verbose_name='Data da coleta',
                                       validators=[validators.prevent_future_date, validators.only_after_2020],
                                       blank=True, null=True)
    result_date = models.DateField(verbose_name='Data do resultado',
                                   validators=[validators.prevent_future_date, validators.only_after_2020], blank=True,
                                   null=True)
    test_location = models.CharField(verbose_name='Local do teste', max_length=50, blank=True, default='')

    note = models.TextField(verbose_name='Observação', blank=True, default='')
    score = models.PositiveIntegerField(verbose_name='Pontuação', blank=True, default=0)
    medical_referral = models.CharField(verbose_name='Encaminhamento', max_length=1,
                                        choices=choices.medical_referral_choices, blank=True, default='')
    medical_referral_status = models.CharField(verbose_name='Situação', max_length=1,
                                               choices=choices.medical_referral_status_choices, blank=True, default='')
    medical_referral_duration = models.PositiveIntegerField(verbose_name='Quantidade de dias', blank=True, default=0)
    prescription = models.CharField(verbose_name='Prescrição', max_length=1, choices=choices.prescription_choices,
                                    blank=True, default='')
    other_prescription = models.CharField(verbose_name='Outro', max_length=50, blank=True, default='')

    VIRUS_EXPOSURE_SCORE = 10

    def get_absolute_url(self):
        return reverse('monitoring:monitoring-detail', kwargs={'pk': self.pk})

    def get_description(self):
        description = ''
        if self.symptom_set.count() > 0:
            description += 'Apresentou ' + ', '.join([s.get_description() for s in self.symptom_set.all()])
        else:
            description += 'Não apresentou sintomas'

        return description

    def calculate_score(self):
        score = 0
        for symptom in self.symptom_set.all():
            if symptom.symptom in choices.maragogi_symptom_score:
                score += choices.maragogi_symptom_score[symptom.symptom]

        if self.virus_exposure.confirmed_cases:
            score += self.VIRUS_EXPOSURE_SCORE

        self.score = score

    def is_suspect(self):
        return self.score > 5 and self.result != 'PO'

    def is_confirmed(self):
        return self.result == 'PO'

    def is_monitored(self):
        # referral = 'isolamento'
        condition1 = (self.medical_referral == '2')
        # referral_status = 'casa'
        condition2 = (self.medical_referral_status == '1')
        # duration > 0
        condition3 = (self.medical_referral_duration > 0)
        # confirmado
        condition4 = self.is_confirmed()

        return condition1 and condition2 and condition3 and condition4

    def __str__(self):
        return '%s (%s)' % (self.profile, self.created.strftime('%d/%m/%Y'))


class Symptom(models.Model):
    monitoring = models.ForeignKey(Monitoring, models.CASCADE, default=1)
    symptom = models.CharField(verbose_name='Tipo de sintoma', max_length=2, choices=choices.symptom_choices,
                               default='')
    intensity = models.CharField(verbose_name='Intensidade', max_length=1, choices=choices.intensity_choices,
                                 blank=True,
                                 default='L')
    onset = models.DateField(verbose_name='Data do surgimento', blank=True, null=True,
                             validators=[validators.only_after_2020, validators.prevent_future_date])

    def get_description(self):
        return '%s há %d dias' % (self.get_symptom_display(), (datetime.now().date() - self.onset).days)

    def __str__(self):
        try:
            return '%s %s desde %s' % (self.get_symptom_display(), self.get_intensity_display(),
                                       self.onset.strftime('%d/%m/%Y'))
        except:
            return self.get_symptom_display()


class Trip(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE, default=1)
    departure_date = models.DateField(verbose_name='Ida', null=True, blank=True, default=None,
                                      validators=[validators.prevent_future_date])
    return_date = models.DateField(verbose_name='Volta', null=True, blank=True, default=None,
                                   validators=[validators.prevent_future_date])
    state = models.CharField(verbose_name='Estado', max_length=2, default='')
    county = models.CharField(verbose_name='Município', max_length=50, default='')

    def __str__(self):
        departure_date = self.departure_date.strftime(
            '%d/%m/%Y') if self.departure_date is not None else '(Não informado)'
        return_date = self.return_date.strftime('%d/%m/%Y') if self.return_date is not None else '(Não informado)'
        return '%s - %s, de %s a %s' % (self.county, self.state, departure_date, return_date)


class Request(models.Model):
    material = models.CharField(verbose_name='Material requisitado', default='', max_length=100)
    quantity = models.PositiveIntegerField(verbose_name='Quantidade necessária', validators=[MinValueValidator(1)])
    name = models.CharField(verbose_name='Nome', default='', max_length=100)
    user = models.ForeignKey(Account, models.SET_NULL, null=True)
    cellphone = models.CharField(verbose_name='Telefone', default='', max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name='E-mail', default='', max_length=40, null=True, blank=True)
    unidade = models.ForeignKey(HealthCenter, models.CASCADE, default=1)


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Neighbourhood(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.city.__str__() + ', ' + self.name


class ActionLog(models.Model):
    action = models.CharField(max_length=1, choices=choices.action_choices)
    user = models.ForeignKey(Account, models.SET_NULL, null=True)
    ip = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    additional_info = models.TextField(verbose_name='Informações adicionais', default='')

    # GenericForeignKey: https://docs.djangoproject.com/en/3.0/ref/contrib/contenttypes/#django.contrib.contenttypes.fields.GenericForeignKey
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(default='0')
    content_object = GenericForeignKey()

    def __str__(self):
        return "(%s) [%s] em %s por %s" % (self.get_action_display(), self.content_type, self.content_object or "(DELETADO)", self.user)


class Family(models.Model):
    pass


# FICHA DE REGISTRO INDIVIDUAL - CASOS DE SÍNDROME RESPIRATÓRIA AGUDA GRAVE HOSPITALIZADO
#
# https://www.cevs.rs.gov.br/upload/arquivos/201903/25141516-1-ficha-srag-hospital.pdf

class SARSHospitalized(models.Model):
    fill_date = models.DateField(verbose_name='Data do preenchimento da ficha de notificação', auto_now_add=True)
    symptom_onset_date = models.DateField(verbose_name='Data de 1ºs sintomas da SRAG', blank=True, null=True)

    health_center = models.ForeignKey(verbose_name='Unidade de saúde', to=HealthCenter, on_delete=models.CASCADE)
    # Dados do paciente
    profile = models.ForeignKey(verbose_name='Paciente', to=Profile, on_delete=models.CASCADE)
    ethnicity = models.CharField(verbose_name='Raça/Cor', max_length=1, choices=choices.ethnicity_choices, blank=True,
                                 default='')
    indian_ethnicity = models.CharField(verbose_name='Etnia indígena', max_length=50, blank=True, default='')
    pregnancy = models.CharField(verbose_name='Gestante', max_length=1, choices=choices.pregnancy_choices, blank=True,
                                 default='')
    schooling = models.CharField(verbose_name='Escolaridade', max_length=1, choices=choices.schooling_choices,
                                 blank=True, default='')
    # Dados de residência
    address = models.ForeignKey(verbose_name='Endereço', to=Address, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(verbose_name='Telefone', max_length=11, blank=True, default='')
    zone = models.CharField(verbose_name='Zona', max_length=1, choices=choices.zone_choices, blank=True, default='')
    country = models.CharField(verbose_name='País', max_length=3, choices=choices.country_choices, blank=True,
                               default='')
    # Dados clínicos e epidemiológicos
    evolved_to_SARS = models.BooleanField(verbose_name='Caso proveniente de surto de SG que evoluiu para SRAG',
                                          blank=True, default=False)
    SARS_from_hospital_internment = models.BooleanField(
        verbose_name='Caso proveniente de surto de SG que evoluiu para SRAG', blank=True, default=False)
    contact_with_poultry_and_pigs = models.BooleanField(verbose_name='Contato com aves ou suínos', blank=True,
                                                        default=True)
    symptoms = BitField(verbose_name='Sinais e sintomas', flags=choices.maragogi_symptoms_choices, blank=True,
                        default=0)
    other_symptoms = models.CharField(verbose_name='Outros sintomas', max_length=50, blank=True, default='')
    comorbidities = BitField(verbose_name='Fatores de risco/Comorbidades', flags=choices.maragogi_comorbidities_choices,
                             blank=True, default=0)
    other_comorbidities = models.CharField(verbose_name='Outras comorbidades', max_length=50, blank=True, default='')
    swine_flu_vaccine = models.BooleanField(verbose_name='Recebeu a vacina contra gripe suína na última campanha')
    mother_vaccinated = models.BooleanField(verbose_name='A mãe recebeu a vacina', blank=True, default=False)
    mother_vaccinated_date = models.DateField(verbose_name='Data em que a mãe recebeu a vacina', blank=True,
                                              default=False)
    breastfeed = models.BooleanField(verbose_name='A mãe amamenta a criança', blank=True, default=False)
    single_dose_date = models.DateField(verbose_name='Data da dose única', blank=True, null=True)
    first_dose_date = models.DateField(verbose_name='Data da 1ª dose', blank=True, null=True)
    second_dose_date = models.DateField(verbose_name='Data da 2ª dose', blank=True, null=True)
    # Dados de atendimento
    flu_antiviral_used = models.BooleanField(verbose_name='Usou antiviral para gripe', blank=True, default=False)
    flu_antiviral = models.CharField(verbose_name='Antiviral', max_length=1, choices=choices.antiviral_choices,
                                     blank=True, default='')
    other_flu_antiviral = models.CharField(verbose_name='Outro antiviral', max_length=30, blank=True, default='')
    flu_treatment_begin_date = models.DateField(verbose_name='Data de início do tratamento', blank=True, null=True)
    internment = models.BooleanField(verbose_name='Houve internação', blank=True, default=False)
    SARS_internment_date = models.DateField(verbose_name='Data da internação por SRAG', blank=True, null=True)
    internment_health_center = models.ForeignKey(verbose_name='Unidade de saúde da internação', to=HealthCenter,
                                                 on_delete=models.CASCADE),
    icu_internment = models.BooleanField(verbose_name='Internado em UTI', blank=True, default=False)
    icu_internment_begin_date = models.DateField(verbose_name='Data da entrada na UTI', blank=True, default=False)
    icu_internment_release_date = models.DateField(verbose_name='Data da saída da UTI', blank=True, default=False)
    ventilatory_support = models.CharField(verbose_name='Uso de suporte ventilatório', max_length=1,
                                           choices=choices.ventilatory_support_choices, blank=True, default='')
    chest_x_ray = models.CharField(verbose_name='Raio X do tórax', max_length=1, choices=choices.chest_x_ray_choices,
                                   blank=True, default=True)
    other_chest_x_ray_result = models.CharField(verbose_name='Outro resultado', max_length=30, blank=True, default='')
    chest_x_ray_date = models.DateField(verbose_name='Data do raio X', blank=True, null=True)
    collected_sample = models.BooleanField(verbose_name='Coletou amostra', blank=True, default=False)
    collection_date = models.DateField(verbose_name='Data da coleta', blank=True, null=True)
    sample_type = models.CharField(verbose_name='Tipo de amostra', max_length=1, choices=choices.sample_type_choices,
                                   blank=True, default='')
    other_sample_type = models.CharField(verbose_name='Outro tipo', max_length=20, blank=True, default='')
    # Dados laboratoriais
    gal = models.TextField(verbose_name='Nº de requisição do GAL', blank=True, default=True)
    if_result = models.CharField(verbose_name='Resultado da IF', max_length=1, choices=choices.if_result_choices,
                                 blank=True, default='')
    if_result_date = models.DateField(verbose_name='Data do resultado da IF', blank=True, null=True)
    if_influenza_result = models.CharField(verbose_name='Positivo para influenza', max_length=1,
                                           choices=choices.influenza_result_choices, blank=True, default='')
    if_respiratory_viruses = BitField(verbose_name='Outros vírus respiratórios',
                                      flags=choices.if_other_respiratory_viruses_choices, blank=True, default=0)
    if_other_respiratory_virus = models.CharField(verbose_name='Outro', max_length=30, blank=True, default='')
    if_laboratory = models.CharField(verbose_name='Laboratório que realizou IF', max_length=30, blank=True, default='')
    if_laboratory_cnes = models.CharField(verbose_name='Código (CNES)', max_length=7, blank=True, default='')
    rt_pcr_result = models.CharField(verbose_name='Resultado da RT-PCR', max_length=1,
                                     choices=choices.rt_pcr_result_choices, blank=True, default='')
    rt_pcr_result_date = models.DateField(verbose_name='Data do resultado da RT-PCR', blank=True, null=True)
    rt_pcr_influenza_result = models.CharField(verbose_name='Positivo para influenza', max_length=1,
                                               choices=choices.influenza_result_choices, blank=True, default='')
    rt_pcr_influenza_a_subtype = models.CharField(verbose_name='Subtipo influenza A', max_length=1,
                                                  choices=choices.rt_pcr_influenza_a_subtype_choices, blank=True,
                                                  default='')
    other_rt_pcr_influenza_a_subtype = models.CharField(verbose_name='Outro subtipo', max_length=20, blank=True,
                                                        default='')
    rt_pcr_influenza_b_subtype = models.CharField(verbose_name='Subtipo influenza B', max_length=1,
                                                  choices=choices.rt_pcr_influenza_b_lineage_choices, blank=True,
                                                  default='')
    other_rt_pcr_influenza_b_subtype = models.CharField(verbose_name='Outro subtipo', max_length=20, blank=True,
                                                        default='')
    rt_pcr_respiratory_viruses = BitField(verbose_name='Outros vírus respiratórios',
                                          flags=choices.rt_pcr_other_respiratory_viruses_choices, blank=True, default=0)
    rt_pcr_other_respiratory_virus = models.CharField(verbose_name='Outro', max_length=30, blank=True, default='')
    rt_pcr_laboratory = models.CharField(verbose_name='Laboratório que realizou IF', max_length=30, blank=True,
                                         default='')
    rt_pcr_laboratory_cnes = models.CharField(verbose_name='Código (CNES)', max_length=7, blank=True, default='')
    # Conclusão
    final_classification = models.CharField(verbose_name='Classificação final do caso', max_length=1,
                                            choices=choices.final_classification_choices, blank=True, default='')
    other_final_classification = models.CharField(verbose_name='Outro agente etiológico', max_length=20, blank=True,
                                                  default='')
    closure_criteria = models.CharField(verbose_name='Critério de encerramento', max_length=1,
                                        choices=choices.closure_criteria_choices, blank=True, default='')
    release_or_death_date = models.DateField(verbose_name='Data da alta ou óbito', blank=True, null=True)
    closure_date = models.DateField(verbose_name='Data do encerramento', blank=True, null=False)
    #
    notes = models.TextField(verbose_name='Observações', blank=True, default='')
    #
    health_professional = models.ForeignKey(verbose_name='Profissional da saúde responsável', to=Account,
                                            on_delete=models.SET_NULL, null=True)
    crm = models.CharField(verbose_name='CRM', max_length=7, blank=True, default='')


class Hospitalization(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    entry = models.DateField(
        verbose_name='Data de entrada', blank=True, null=True,
        validators=[validators.only_after_2020, validators.prevent_future_date]
    )
    departure = models.DateField(
        verbose_name='Data de saída', blank=True, null=True,
        validators=[validators.only_after_2020, validators.prevent_future_date]
    )
    bed_type = models.CharField(
        verbose_name='Tipo de internação', blank=True, null=True,
        max_length=1, choices=choices.hospitalization_choices,
        default=''
    )
    health_center = models.ForeignKey(
        verbose_name='Unidade de saúde', blank=True, null=True,
        to=HealthCenter, on_delete=models.SET_NULL
    )

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        entry = self.entry.strftime(
            '%d/%m/%Y') if self.entry is not None else '(Não informado)'
        departure = self.departure.strftime('%d/%m/%Y') if self.departure is not None else '(Não informado)'
        return '%s <br>Internação em %s, de %s a %s' % (
            self.health_center, self.get_bed_type_display(), entry, departure)

class Contact(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    name = models.CharField(verbose_name='Nome', max_length=100)
    cpf = models.CharField(verbose_name='CPF', max_length=11, blank=True, default='',
                           validators=[validators.only_digits, validators.validate_cpf])
    phone_number = models.CharField(verbose_name='Telefone', max_length=11)
    contact_date = models.DateField(verbose_name='Data do Contato',
                                    validators=[validators.only_after_2020, validators.prevent_future_date])
    recurring_contact = models.BooleanField(verbose_name='Tem contato frequentemente', default=False)

    created = models.DateTimeField(editable=False)

    def __str__(self):
        phone_number = self.phone_number
        formated_number = ''
        if len(phone_number) == 11:
            formated_number = '('+phone_number[0:2]+') '+phone_number[2:7]+'-'+phone_number[7:11]
        else:
            formated_number = '('+phone_number[0:2]+') '+phone_number[2:6]+'-'+phone_number[6:10]
        contact_date = self.contact_date.strftime('%d/%m/%Y')
        return 'Contato com {}, Nº de telefone: {}, em {}'.format(self.name, formated_number, contact_date)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super().save(*args, **kwargs)


class Vaccination(models.Model):
    dose_choices = (
        ('0', 'Única'),
        ('1', 'Primeira'),
        ('2', 'Segunda'),
    )

    vaccine_choices = (
        ('cb', 'CoronaVac/Butantan'),
        ('of', 'Oxford/Fiocruz'),
        ('co', 'Aliança Covax/OMS'),
        ('cx', 'Covaxin'),
        ('pb', 'Pfizer/BioNTech'),
        ('mo', 'Moderna'),
        ('jj', 'Johnson/Janssen'),
        ('sv', 'Sputnik V'),
    )

    profile = models.ForeignKey(Profile, models.CASCADE)
    date = models.DateField(verbose_name='Data de vacinação',
                            validators=[validators.prevent_future_date, validators.only_after_2021])
    dose = models.CharField(verbose_name='Dose', max_length=1, choices=dose_choices)
    vaccine = models.CharField(verbose_name='Vacina', max_length=2, choices=vaccine_choices)

    def __str__(self):
        return '{}, em {}, Dose: {}.'.format(self.get_vaccine_display(), str(self.date), self.get_dose_display())
