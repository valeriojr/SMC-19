import json
from datetime import datetime, timedelta

import pandas
from django import views
from django.contrib.auth import mixins
from django.db import connection
from django.db.models import Sum, Count, Q
from django.db.models.functions import ExtractWeek
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from django.views import generic

import utils
from dashboard import models, forms
from dashboard.models import EpidemiologicalReport
from monitoring.models import Profile, Monitoring, Hospitalization
from .utils import get_previsao_leitos, generate_df_daily_avg


# Create your views here.


class Dashboard(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self):
        context = super(Dashboard, self).get_context_data()
        g = self.request.user.group

        context.update(
            Profile.objects.filter(group=g).annotate(**Profile.get_status(timezone.now())).aggregate(
                Sum('confirmed'), Sum('recovered'), Sum('suspect'), Sum('monitored'), Sum('dead')
            )
        )

        last_4_weeks = timedelta(weeks=4)
        for status in ('confirmed', 'recovered'):
            last_4_weeks_status = pandas.DataFrame(
                Profile.objects.filter(group=g)
                    .filter(**{
                        status + '_date__gte': timezone.now() - last_4_weeks,
                        status + '_date__lte': timezone.now(),
                    })
                    .annotate(**Profile.get_status(timezone.now()), week=ExtractWeek(f'{status}_date'))
                    .order_by()
                    .values('week')
                    .annotate(
                    Sum(status)
                )
                    .order_by('week')
            )

            try:
                last_4_weeks_status.week = last_4_weeks_status.week.apply(
                    lambda w: datetime.strptime(f'{datetime.now().year}-{w-1}-1', "%Y-%W-%w").strftime('%d/%m'))
            except:
                pass
            context[f'last_4_weeks_{status}'] = last_4_weeks_status.to_dict(orient='list')

        previsoes_leitos = get_previsao_leitos(g)
        context['dados_previsao'] = {
            'dias': [datetime.now().date() + timedelta(days=i) for i in range(4)],
            'previsoes': previsoes_leitos
        }

        context['genderData'] = pandas.DataFrame((Profile.objects
                                                  .filter(group=g)
                                                  .order_by()
                                                  .annotate(**models.Profile.get_status(timezone.now()))
                                                  .values('gender')
                                                  .annotate(Sum('confirmed'))).order_by('gender')).to_dict('list')

        df_monitoring_daily = pandas.DataFrame(
            Monitoring.objects
                .filter(health_center__group=g)
                .order_by()
                .values('attendance_date')
                .annotate(count=Count('attendance_date'))
                .order_by('attendance_date')
        )
        df_monitoring_daily = generate_df_daily_avg(df_monitoring_daily, 'attendance_date', 7)

        df_confirmed_daily = pandas.DataFrame(
            Profile.objects
                .filter(group=g)
                .filter(confirmed_date__isnull=False)
                .order_by()
                .values('confirmed_date')
                .annotate(count=Count('confirmed_date'))
                .order_by('confirmed_date')
        )
        df_confirmed_daily = generate_df_daily_avg(df_confirmed_daily, 'confirmed_date', 7)

        df_tests_daily = pandas.DataFrame(
            Monitoring.objects
                .filter(health_center__group=g)
                .filter(Q(tests='TR') | Q(tests='RT') | Q(tests='A'))
                .order_by()
                .values('attendance_date')
                .annotate(count=Count('attendance_date'))
                .order_by('attendance_date')
        )
        df_tests_daily = generate_df_daily_avg(df_tests_daily, 'attendance_date', 7)

        context['hospitalization'] = pandas.DataFrame(
            Hospitalization.objects
                .filter(profile__group=g)
                .order_by()
                .values('entry')
                .annotate(common=Count('bed_type', filter=Q(bed_type='2')),
                          icu=Count('bed_type', filter=Q(bed_type='3')))
        ).to_dict(orient='list')

        date_form = forms.DateFilter(self.request.GET)
        context['date_form_to_mvg'] = date_form

        if date_form.is_valid():
            start_date = date_form.cleaned_data['start_date']
            end_date = date_form.cleaned_data['end_date']
            if start_date:
                start_date = datetime.strftime(start_date, "%Y-%m-%d")
                df_monitoring_daily = df_monitoring_daily.loc[df_monitoring_daily['attendance_date']>=start_date]
                df_tests_daily = df_tests_daily.loc[df_tests_daily['attendance_date']>=start_date]
                df_confirmed_daily = df_confirmed_daily.loc[df_confirmed_daily['confirmed_date']>=start_date]
            if end_date:
                end_date = datetime.strftime(end_date, "%Y-%m-%d")
                df_monitoring_daily = df_monitoring_daily.loc[df_monitoring_daily['attendance_date']<=end_date]
                df_tests_daily = df_tests_daily.loc[df_tests_daily['attendance_date']<=end_date]
                df_confirmed_daily = df_confirmed_daily.loc[df_confirmed_daily['confirmed_date']<=end_date]

        context['monitoring_daily'] = df_monitoring_daily.to_dict(orient='list')
        context['tests_daily'] = df_tests_daily.to_dict(orient='list')
        context['confirmed_daily'] = df_confirmed_daily.to_dict(orient='list')

        return context


class CasesPerStatus(mixins.LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        group_by = self.request.GET.get('group-by', '')

        if group_by == '':
            return HttpResponse('')
        elif group_by not in ['gender', 'smoker', 'vaccinated', 'oxygen', 'age']:
            return HttpResponseForbidden()

        status_conditions = {
            'confirmed': "monitoring_monitoring.result = 'PO'",
            'suspect': 'monitoring_monitoring.score > 5',
            'deaths': "monitoring_monitoring.result = 'M'",
        }

        status = self.request.GET.get('status')
        if status not in status_conditions:
            return HttpResponseForbidden()

        status_condition = status_conditions[status]

        sql_query = '''
        SELECT monitoring_profile.%s AS label, SUM(CASE  WHEN %s THEN 1 ELSE 0 END) AS value 
        FROM monitoring_profile 
        JOIN 
            (SELECT monitoring_monitoring.profile_id, MAX(monitoring_monitoring.id) AS latest_id 
            FROM monitoring_monitoring 
            GROUP BY monitoring_monitoring.profile_id) last_monitorings 
        ON monitoring_profile.id = last_monitorings.profile_id 
        JOIN monitoring_monitoring ON last_monitorings.latest_id = monitoring_monitoring.id
        JOIN monitoring_address ON monitoring_profile.id = monitoring_address.profile_id
        WHERE monitoring_address.`primary` = 1 
        GROUP BY monitoring_profile.%s''' % (group_by, status_condition, group_by)

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            confirmed_cases = utils.dictfetchall(cursor)

        for row in confirmed_cases:
            row['value'] = float(row['value'] if row['value'] is not None else 0)

        try:
            choices = dict(globals()['%s_choices' % group_by])
        except KeyError:
            choices = None

        if choices:
            for row in confirmed_cases:
                try:
                    row['label'] = choices[row['label']]
                except KeyError:
                    pass

        return HttpResponse(json.dumps(confirmed_cases))


class EpidemiologicalReport(generic.FormView):
    template_name = 'dashboard/epidemiological_report.html'

    def get_initial(self):
        initial = super(EpidemiologicalReport, self).get_initial()
        initial['date__lte'] = datetime.now().date()

        return initial

    def get_form(self, form_class=None):
        return forms.EpidemiologicalReportForm(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super(EpidemiologicalReport, self).get_context_data()

        form = self.get_form()

        if form.is_valid():
            filters = {k: v for k, v in form.cleaned_data.items() if v is not None}
        else:
            filters = {}

        stats = models.EpidemiologicalReport.objects.filter(group__name=self.kwargs['group'], **filters).order_by(
            '-date').values()

        context['stats'] = list(reversed(stats))
        context['total'] = pandas.DataFrame(data=stats).sum().to_dict()
        context['total']['monitored'] = Profile.objects.filter(group__name=self.kwargs['group'], monitored_date__gt=timezone.now().date(),
                                                               death_date__isnull=True).count()
        context['group'] = self.kwargs['group']
        context['last_update'] = models.EpidemiologicalReport.objects.filter(group__name=self.kwargs['group']).order_by("date").last().date

        return context
