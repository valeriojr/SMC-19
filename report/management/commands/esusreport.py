import time
from datetime import datetime

import pandas
import numpy as np
from django.core.management import BaseCommand
from django.db.models import Max, F, Q, Case, When, Value, CharField, Count
from rest_framework import serializers

from monitoring.models import *

pandas.set_option('display.max_columns', 500)


class ESusSerializer(serializers.Serializer):
    pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        last_monitorings = Monitoring.objects.annotate(
            nome_completo=F('profile__full_name'),
            nome_completo_mae=F('profile__mother_name'),
            data_de_nascimento=F('profile__birth_date'),
            tel_celular=F('profile__phone_number'),
            data_inicio = F('profile__first_symptom_onset'),
            data_de_coleta = F('profile__monitoring__collection_date'),
            tipo_teste = F('profile__monitoring__tests'),
            resultado_teste = F('profile__monitoring__result'),
            data_do_resultado = F('profile__monitoring__result_date'),
            tem_CPF=Case(
                When(Q(profile__cpf__isnull=False) & ~Q(profile__cpf=11 * '0'),
                     then=Value('S', output_field=CharField())),
                When(Q(profile__cpf__isnull=True) | Q(profile__cpf=11 * '0'),
                     then=Value('N', output_field=CharField())),
            ),
            teste=Case(
                When(collection_date__isnull=True, then=Value('', output_field=CharField())),
                When(result_date__isnull=True, then=Value('COLETADO', output_field=CharField())),
                When(result_date__lte=datetime.now().date(), then=Value('CONCLUÍDO', output_field=CharField()))
            ),
            profissional_de_seguranca=F('profile__security_professional'),
            criacao = F('profile__monitoring__created'),
            data_de_atendimento=F('profile__monitoring__attendance_date'),
            CPF=F('profile__cpf'),
            cns=F('profile__cns'),
            cbo=F('profile__cbo'),
            passaporte=F('profile__passport'),
            pais_de_origem=F('profile__birthplace'),
            sexo=F('profile__gender'),
            raca=F('profile__ethnicity'),
            comorbidades=F('profile__comorbidities'),
            cep=F('profile__address__postal_code'),
            logradouro=F('profile__address__street_name'),
            numero=F('profile__address__number'),
            complemento=F('profile__address__complement'),
            bairro=F('profile__address__neighbourhood'),
            municipio=F('profile__address__city'),
            uf=F('profile__address__state'),
            # Grupo
            grupo = F('profile__group_id'),
            # Sintomas
            febre=Count('symptom', Q(symptom__symptom='FV')),
            tosse=Count('symptom', Q(symptom__symptom='TS') | Q(symptom__symptom='TP')),
            dor_garganta=Count('symptom', Q(symptom__symptom='ST')),
            dispneia=Count('symptom', Q(symptom__symptom='SB')),
            outro=F('symptom__symptom')
        ).filter(profile__address__primary=True)

        df = pandas.DataFrame(last_monitorings.values())

        def merge_symptoms(ol):
            try:
                d = dict(choices.symptom_choices)
                ol = filter(lambda x: x not in ('FV', 'TS', 'TP', 'ST', 'SB'), ol)
                ol = map(lambda x: d[x], ol)
                return ', '.join(ol)
            except:
                return None

        #print(df.groupby('profile_id')['outro'].apply(merge_symptoms))
        grouped = df.groupby('profile_id')
        df = df.merge(grouped.outro.apply(merge_symptoms), on='profile_id')
        df = df.sort_values(by=['criacao'])
        df = df.drop_duplicates(subset = ['profile_id'], keep='last')
        df.drop_duplicates(subset=df.columns.difference(['outro_x']), inplace=True)
        
        for (column, bit) in [('respiratoria_cronica', 0), ('renal_cronica', 8), ('diabetes', 5), ('cromossomica', 17),
                              ('imunosupressao', 11), ('cardiaca_cronica', 6), ('gestante_risco', 16), ('obesidade', 14)]:
            df[column] = df.comorbidades.apply(lambda c: 'S' if c & 1 << bit else 'N')

        print(df[df.cardiaca_cronica == 'S'].count())
		
        df = self.drop_columns(df)
        df = self.rename_columns(df)
        df.astype('str')
        df_maragogi = df.loc[df['grupo']==1]
        df_dois_riachos = df.loc[df['grupo']==2]
        df_campo_alegre = df.loc[df['grupo']==3]

        df_maragogi.to_csv(f'e-sus-report-maragogi-{datetime.now().strftime("%H-%M-%S-%d-%m-%Y")}.csv', index=False, sep=';')
        df_dois_riachos.to_csv(f'e-sus-report-dois-riachos-{datetime.now().strftime("%H-%M-%S-%d-%m-%Y")}.csv', index=False, sep=';')
        df_campo_alegre.to_csv(f'e-sus-report-campo-alegre-{datetime.now().strftime("%H-%M-%S-%d-%m-%Y")}.csv', index=False, sep=';')

    def rename_columns(self, df):
        df = df.rename(columns={
            'outro_y': 'outro',
        })

        return df

    def drop_columns(self, df):
        df.drop(columns=
                'id,attendance_date,status,virus_exposure,oxygen_saturation,temperature,pulse,blood_pressure,created,collection_date,tests,result_date,result,'
                'professional,health_center_id,created_by_id,community_health_agent_name,hypothesis,'
				'test_location,note,score,medical_referral,medical_referral_status,medical_referral_duration,'
                'prescription,other_prescription,outro_x'.split(','), errors='coerce', inplace=True)
        return df

    def get_test_state(self, collection, result):
        if collection is None:
            return ''
        if result is None:
            return 'COLETADO'
        if result <= datetime.now().date():
            return 'CONCLUÍDO'
        return ''
