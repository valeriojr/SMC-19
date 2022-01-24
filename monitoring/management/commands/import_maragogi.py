from datetime import datetime

import pandas
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand

from monitoring import models, choices

from unidecode import unidecode

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', nargs=1, type=str)

    def handle(self, *args, **options):
        df = pandas.read_excel(options['path'][0],
                               dtype={
                                   'CPF ou CNS do paciente': str,
                                   'Telefone de contato': str,
                                   'hipótese Diagnóstica': str,
                                   'Hipótese Diagnóstica, houve notificação para COVID-19?': str,
                                   'Data de Nascimento': str,
                               },
                               parse_dates=['Data da Consulta'])
        df = df.fillna('')
        df.apply(self.populate_row, axis='columns')

    def populate_row(self, row):
        self.create_symptoms(row, self.create_monitoring(row, self.create_profile(row)))

    def create_profile(self, row):
        cpf = row['CPF ou CNS do paciente'] if len(row['CPF ou CNS do paciente']) <= 11 else ''
        cns = row['CPF ou CNS do paciente'] if len(row['CPF ou CNS do paciente']) > 11 else ''
        try:
            birth_date = row['Data de Nascimento'].replace('/', '')
            birth_date = datetime(day=int(birth_date[:2]), month=int(birth_date[2:4]),
                                  year=int(birth_date[4:] if len(birth_date) - 4 == 4 else '19' + birth_date[4:]))
        except:
            birth_date = None
        phone = row['Telefone de contato']
        for c in '-() ':
            phone = phone.replace(c, '')
        try:
            age = relativedelta(datetime.now().date(), birth_date).years
        except:
            age = 0

        profile = models.Profile.objects.create(
            full_name=row['Nome do Paciente'],
            cpf=cpf,
            cns=cns,
            birth_date=birth_date,
            phone_number=phone,
            age=age,
        )

        models.Address.objects.create(city='MARAGOGI', primary=True, profile=profile)

        return profile

    def create_monitoring(self, row, profile):
        tests_dict = {value: key for key, value in choices.tests_choices}
        tests_dict[''] = ''

        centers = models.HealthCenter.objects.filter(
            center_name__contains=unidecode(row['Unidade Básica de Saúde'][4:].split('-')[0].strip(' ')))

        if len(centers) > 0:
            center = sorted(centers, key=lambda x: len(str(x)), reverse=True)[0]  # Unidade de saúde com mais informação
        else:
            center = None

        monitoring = models.Monitoring.objects.create(
            profile=profile,
            community_health_agent_name=row['Nome do Agente Comunitário de Saúde'],
            professional=row['Nome do Profissional'],
            hypothesis=row['hipótese Diagnóstica'] + ' ' + row[
                'Hipótese Diagnóstica, houve notificação para COVID-19?'],
            note=row['Observação'],
            score=row['Pontuação'],
            tests=tests_dict[row['Foi solicitado exames diagnósticos para o COVID-19?']],
            health_center=center
        )

        monitoring.created = row['Data da Consulta']
        monitoring.save()

        return monitoring

    def create_symptoms(self, row, monitoring):
        symptoms_dict = {
            'Tem febre?': 'FV',
            'Tem dor de cabeça?': 'DC',
            'Tem secreção nasal ou coriza?': 'CN',
            'Tem dor/irritação de garganta?': 'ST',
            'Tem tosse seca?': 'TS',
            'Tem dificuldade respiratória?': 'SB',
            'Tem confusão mental?': 'CM',
            'Tem Conjuntivite?': 'CJ',
            'Tem Anosmia?': 'AN',
        }

        if row['Esteve em contato, nos últimos 14 dias com alguém diagnosticado com COVID 19?'].lower() == 'sim':
            monitoring.virus_exposure = models.Monitoring.virus_exposure.confirmed_cases
            monitoring.save()

        symptoms = []

        for symptom, code in symptoms_dict.items():
            if row[symptom].lower() == 'sim':
                symptoms.append(models.Symptom(symptom=code, monitoring=monitoring))

        models.Symptom.objects.bulk_create(symptoms)
