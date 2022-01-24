import django_filters
from django.db.models import Q
from django.forms import CheckboxSelectMultiple
from django.utils import timezone

from monitoring.choices import tests_choices, address_type_choices, symptom_choices
from monitoring.models import Profile, Monitoring, Address
from prediction.models import HealthCenter
from report import choices


class ProfileReportFilters(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = []

    report_type = django_filters.ChoiceFilter(label='Tipo de relatório', choices=choices.report_type_choices,
                                              method='filter_report_type')
    status = django_filters.ChoiceFilter(label='Status', choices=choices.status_choices, method='filter_status')
    tests = django_filters.ChoiceFilter(label='Testes realizados', choices=tests_choices, method='filter_tests')
    o2_saturation = django_filters.NumberFilter(label='Saturação de O<sub>2</sub>', method='filter_o2_saturation')

    def filter_report_type(self, queryset, name, value):
        return queryset

    def filter_status(self, queryset, name, value):
        if value == 'confirmed':
            return queryset.filter(confirmed_date__lte=timezone.now(), death_date__isnull=True)
        elif value == 'suspect':
            return queryset.filter(suspect_date__lte=timezone.now(), discarded_date__isnull=True)
        elif value == '':
            return queryset

    def filter_tests(self, queryset, name, value):
        if value:
            return queryset.filter(monitoring__tests=value).distinct()

        return queryset

    def filter_o2_saturation(self, queryset, name, value):
        return queryset.filter(monitoring__oxygen_saturation__gt=0.0,
                               monitoring__oxygen_saturation__lte=value).distinct()


class MonitoringReportFilters(django_filters.FilterSet):
    class Meta:
        model = Monitoring
        fields = []

    report_type = django_filters.ChoiceFilter(label='Tipo de relatório', choices=choices.report_type_choices,
                                              method='filter_report_type')
    attendance_date__range = django_filters.DateFromToRangeFilter(label='Intervalo (data do atendimento)',
                                                                  method='filter_attendance_date',
                                                                  widget=django_filters.widgets.RangeWidget(attrs={
                                                                      'type': 'date',
                                                                  }))
    health_center = django_filters.ModelChoiceFilter(label='Unidade de saúde')
    status = django_filters.ChoiceFilter(label='Status', choices=choices.status_choices, method='filter_status')
    tests = django_filters.ChoiceFilter(label='Testes realizados', choices=tests_choices, method='filter_tests')
    o2_saturation = django_filters.NumberFilter(label='Saturação de O<sub>2</sub>', method='filter_o2_saturation')
    symptoms = django_filters.MultipleChoiceFilter(label='Sintomas apresentados', choices=symptom_choices,
                                                   widget=CheckboxSelectMultiple, method='filter_symptoms')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['health_center'].queryset = HealthCenter.objects.filter(group=request.user.group)

    def filter_report_type(self, queryset, name, value):
        return queryset

    def filter_status(self, queryset, name, value):
        if value == 'confirmed':
            return queryset.filter(result='PO')
        elif value == 'suspect':
            return queryset.filter(score__gte=5, result='SR')
        elif value == '':
            return queryset

    def filter_tests(self, queryset, name, value):
        if value:
            return queryset.filter(tests=value)

        return queryset

    def filter_o2_saturation(self, queryset, name, value):
        return queryset.filter(oxygen_saturation__gt=0.0, oxygen_saturation__lte=value)

    def filter_attendance_date(self, queryset, name, value):
        if value.start is not None:
            print('start', value.start)
            queryset = queryset.filter(attendance_date__gte=value.start)
        if value.stop is not None:
            print('stop', value.stop)
            queryset = queryset.filter(attendance_date__lte=value.stop)

        return queryset

    def filter_symptoms(self, queryset, name, value):
        print(name, value)
        query = Q()

        for symptom in value:
            query |= Q(symptom__symptom=symptom)

        queryset = queryset.filter(query).distinct()

        return queryset


class AddressReportFilters(django_filters.FilterSet):
    class Meta:
        model = Address
        fields = []

    report_type = django_filters.ChoiceFilter(label='Tipo de relatório', choices=choices.report_type_choices,
                                              method='filter_report_type')
    type = django_filters.ChoiceFilter(label='Tipo de endereço', choices=address_type_choices)
    status = django_filters.ChoiceFilter(label='Status', choices=choices.status_choices, method='filter_status')
    tests = django_filters.ChoiceFilter(label='Testes realizados', choices=tests_choices, method='filter_tests')
    o2_saturation = django_filters.NumberFilter(label='Saturação de O<sub>2</sub>', method='filter_o2_saturation')

    def filter_report_type(self, queryset, name, value):
        return queryset

    def filter_status(self, queryset, name, value):
        if value == 'confirmed':
            return queryset.filter(profile__confirmed_date__lte=timezone.now(), profile__death_date__isnull=True)
        elif value == 'suspect':
            return queryset.filter(profile__suspect_date__lte=timezone.now(), profile__discarded_date__isnull=True)
        elif value == '':
            return queryset

    def filter_tests(self, queryset, name, value):
        if value:
            return queryset.filter(tests=value).distinct()

        return queryset

    def filter_o2_saturation(self, queryset, name, value):
        return queryset.filter(oxygen_saturation__gt=0.0, oxygen_saturation__lte=value).distinct()
