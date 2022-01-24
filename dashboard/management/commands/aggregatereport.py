import datetime

from django.core.management import BaseCommand
from django.db.models import Sum, Min

from accounts.models import Group
from dashboard import models
from dashboard import utils
from monitoring.models import Profile
from monitoring.utils import date_flow, mean_diff_attendance_symptom


class Command(BaseCommand):
    help = 'Agrega as estatísticas de atendimentos diários.'

    def add_arguments(self, parser):
        parser.add_argument('-g', '--group', nargs='*', type=str,
                            help='Lista de grupos. Se não especificado o processo é feito em todos os grupos.')
        parser.add_argument('-d', '--date', nargs='*', type=str,
                            help=f'''Data para agregar os dados. Se não especificado o processo é feito em
                             todos os dias e a tabela do informe epidemiológico *será resetada*!''')

    def handle(self, *args, **options):
        if options['date'] is None:
            # recalcula as datas dos eventos e salva nos profiles
            self.run_date_flow()

            # calcula data inicial de agregação dos dados
            profiles = Profile.objects.all()
            initial_date = min(profiles.aggregate(Min('confirmed_date'), Min('recovered_date'),
                                                  Min('suspect_date'), Min('discarded_date'),
                                                  Min('monitored_date'), Min('death_date')).values())

            # define data final de agregação dos dados como ontem
            final_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
        else:
            initial_date = datetime.datetime.strptime(options['date'][0], '%d/%m/%Y').date()
            final_date = initial_date

        if options['group'] is not None:
            all_groups = Group.objects.filter(name__in=options['group'])
            if all_groups.count() == 0:
                print("Nenhum grupo válido informado.")
                return
        else:
            all_groups = Group.objects.all()

        for group in all_groups:
            print(f'Agregando dados do grupo {group}')
            print("Data inicial: ", initial_date)
            print("Data final: ", final_date)

            if options['date'] is None:
                # reseta a contagem quando uma data não é dada
                models.EpidemiologicalReport.objects.filter(group=group).delete() #.update(confirmed=0, suspect=0,
                                                                                  #recovered=0, deaths=0,
                                                                                  #discarded=0, monitored=0)

            date = initial_date
            while date <= final_date:
                #print(f'\tAgregando dados do dia {date}')
                self.save_report(group, date)
                date += datetime.timedelta(days=1)

    def save_report(self, group, date):
        models.EpidemiologicalReport.objects.get_or_create(date=date, group=group)

        data = utils.count_daily(group, date)

        models.EpidemiologicalReport.objects.filter(date=date, group=group).update(**data)

    def run_date_flow(self):
        print("Recalculando as datas de cada paciente.")
        # Filtra os pacientes (a definir filtros) (talv)
        profiles = Profile.objects.filter()

        # reseta as datas, exceto de morte
        profiles.update(suspect_date=None, confirmed_date=None,
                        recovered_date=None, discarded_date=None,
                        monitored_date=None, first_symptom_onset=None,
                        estimated_first_symptom=None)

        # Calcula diferença média entre data de atendimento e primeiro sintoma
        diff_attendance_symptom = mean_diff_attendance_symptom()

        # Executa a rotina para cada atendimento de cada paciente
        for p in profiles:
            for m in p.monitoring_set.order_by('attendance_date'):
                date_flow(p, m, diff_attendance_symptom)

        # Salva as possíveis alterações das datas no banco
        Profile.objects.bulk_update(profiles, ['confirmed_date', 'suspect_date',
                                               'recovered_date', 'discarded_date',
                                               'monitored_date', 'first_symptom_onset',
                                               'estimated_first_symptom'])
