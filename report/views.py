import codecs

import pandas
from django.contrib import messages
from django.contrib.auth import mixins
from django.core.paginator import Paginator
from django.core.exceptions import FieldDoesNotExist
from django.db.models import F, Case, When, Value, IntegerField, Min
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django_filters import views

from monitoring import choices
from monitoring.models import Profile, Monitoring, Address
from report import filters


class ReportView(mixins.LoginRequiredMixin, views.FilterView):
    template_name = 'report/status_report.html'
    filterset_class = filters.ProfileReportFilters
    paginate_by = 25

    def get_filterset(self, filterset_class=None):
        data = self.request.GET if self.request.method == 'GET' else self.request.POST
        report_type = data.get('report_type')
        if report_type == 'profile':
            return filters.ProfileReportFilters(data)
        elif report_type == 'monitoring':
            return filters.MonitoringReportFilters(self.request, data)
        elif report_type == 'address':
            return filters.AddressReportFilters(data)

        return filters.ProfileReportFilters(data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReportView, self).get_context_data(object_list=object_list, **kwargs)

        report_type = self.request.GET.get('report_type')
        columns = {
            'profile': ['Nome completo', 'CPF', 'Data de nascimento', 'Telefone'],
            'monitoring': ['Nome completo', 'CPF', 'Data do atendimento', 'Unidade de saúde', 'Resposta do exame',
                           'Encaminhamento', 'Situação', 'Duração do isolamento'],
            'address': ['Nome completo', 'Tipo de endereço', 'Logradouro', 'Número', 'Complemento', 'Bairro', 'CEP']
        }

        context['columns'] = columns.get(report_type, '')
        context['report_type'] = report_type

        f = self.get_filterset()
        if f.is_valid():
            if report_type == 'profile':
                paginator = Paginator(f.qs.filter(group=self.request.user.group), self.paginate_by)
            elif report_type in ('monitoring', 'address'):
                paginator = Paginator(f.qs.filter(profile__group=self.request.user.group), self.paginate_by)

        context['paginator'] = paginator
        if paginator:
            context['page_obj'] = paginator.get_page(self.request.GET.get('page', 1))

        return context

    def post(self, request):
        filterset = self.get_filterset()
        if filterset.is_valid():
            report_type = self.request.GET.get('report_type')
            portuguese_report_type = {
                'profile': 'pacientes',
                'monitoring': 'atendimentos',
                'address': 'enderecos',
            }.get(report_type, '')

            # Exportar o csv como utf-8 (retirado de https://gist.github.com/marteinn/f3c181add07654c2f3dee88cab9afc91)
            # Force response to be UTF-8 - This is where the magic happens
            response = HttpResponse(content_type='text/csv')
            response.write(codecs.BOM_UTF8)
            response['Content-Disposition'] = f'''attachment;\
                filename="{self.request.user.cpf}-{portuguese_report_type}-{self.request.user.group}-{timezone.now().strftime(
                "%d%m%Y-%H%M%S")}.csv"'''

            data = self.get_filterset().qs
            if report_type in ('monitoring', 'address'):
                # Anota informações do paciente
                data = data.filter(profile__group=self.request.user.group)
                data = data.annotate(full_name=F('profile__full_name'), birth_date=F('profile__birth_date'),
                                     cpf=F('profile__cpf'), mother_name=F('profile__mother_name'),
                                     cns=F('profile__cns'),
                                     phone_number=F('profile__phone_number'),
                                     estimated_first_symptom=F('profile__estimated_first_symptom'),
                                     first_symptom_onset=F('profile__first_symptom_onset'),
                                     suspect_date=F('profile__suspect_date'),
                                     confirmed_date=F('profile__confirmed_date'),
                                     monitored_date=F('profile__monitored_date'),
                                     death_date=F('profile__death_date'),
                                     discarded_date=F('profile__discarded_date'),
                                     recovered_date=F('profile__recovered_date'))
                # Anota a data dos sintomas
                if report_type == 'monitoring':
                    data = data.annotate(**{
                        symptom[1]: Case(
                            When(symptom__symptom=symptom[0], then=Min('symptom__onset'))
                        ) for symptom in choices.symptom_choices
                    })
                    # TODO: fazer o bitfield funcionar
                    # .annotate(**{
                    #     exposure[1]: Case(
                    #         When(virus_exposure=Monitoring.virus_exposure.__getattr__(exposure[0]),
                    #              then=Value(1, output_field=IntegerField()))
                    #     ) for exposure in choices.exposure_choices
                    # })

                    address_fields = {
                        'Tipo de endereço': F('profile__address__type'),
                        'CEP': F('profile__address__postal_code'),
                        'Bairro': F('profile__address__neighbourhood'),
                        'Logradouro': F('profile__address__street_name'),
                        'Número': F('profile__address__number'),
                        'Complemento': F('profile__address__complement'),
                        'Cidade': F('profile__address__city'),
                        'Estado': F('profile__address__state'),
                        'Nº de pessoas que residem nesse endereço': F('profile__address__people'),
                        'primary': F('profile__address__primary')
                    }

                    data = data.annotate(**address_fields).filter(primary=True)

            elif report_type == 'profile':
                # Anota as comorbidades do paciente
                data = data.filter(group=self.request.user.group).annotate(**{
                    comorbidity[1]: Case(
                        When(comorbidities=Profile.comorbidities.__getattr__(comorbidity[0]),
                             then=Value(1, output_field=IntegerField()))
                    ) for comorbidity in choices.comorbidity_choices
                })

            df = pandas.DataFrame(data.values())

            # https://stackoverflow.com/questions/56481300/reorder-certain-columns-in-pandas-dataframe
            if report_type in ('monitoring', 'address'):
                first_cols = ['full_name', 'birth_date', 'cpf', 'mother_name', 'cns', 'phone_number']
                last_cols = [col for col in df.columns if col not in first_cols]
                df = df[first_cols + last_cols]

                if report_type == 'monitoring':
                    for _, symptom in choices.symptom_choices:
                        df[symptom] = pandas.to_datetime(df[symptom], errors='coerce')

                    keep_columns = [col for col in df.columns if col not in dict(choices.symptom_choices).values()]
                    aggregations = {
                        symptom[1]: 'min' for symptom in choices.symptom_choices
                    }

                    symptoms = df.groupby(['id'], as_index=False).aggregate(aggregations)
                    df = df[keep_columns].drop_duplicates().merge(symptoms, on='id')

            # Renomeia as colunas para verbose_name
            # Colunas do profile para o relatório de atendimentos e endereços
            columns_to_rename = {
                'full_name': 'Nome completo',
                'birth_date': 'Data de nascimento',
                'cpf': 'CPF',
                'mother_name': 'Nome da mãe',
                'cns': 'CNS',
                'phone_number': 'Telefone',
                'first_symptom_onset': 'Data dos primeiros sintomas',
                'estimated_first_symptom': 'Estimativa da data dos primeiros sintomas',
                'suspect_date': 'Data de suspeita',
                'confirmed_date': 'Data da confirmação',
                'recovered_date': 'Data da recuperação',
                'monitored_date': 'Data do término do monitoramento',
                'discarded_date': 'Data do descarte',
                'death_date': 'Data do óbito',
            }
            # Procura o verbose_name no respectivo model
            for col in df.columns:
                try:
                    if report_type == 'profile':
                        columns_to_rename[col] = Profile._meta.get_field(col).verbose_name
                    elif report_type == 'monitoring':
                        columns_to_rename[col] = Monitoring._meta.get_field(col).verbose_name
                    elif report_type == 'address':
                        columns_to_rename[col] = Address._meta.get_field(col).verbose_name
                except FieldDoesNotExist:
                    pass
            # Renomeia as colunas, ignorando possíveis erros
            df.rename(columns=columns_to_rename, inplace=True, errors='coerce')

            # Substitui True/False por 1/0 respectivamente
            df.replace(True, 1, inplace=True)
            df.replace(False, 0, inplace=False)

            df.to_csv(response, index=False, encoding='utf-8', sep=';')

            return response
        else:
            messages.error(self.request, filterset.errors)
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('report:status-report')
