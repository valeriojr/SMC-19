from crispy_forms import helper
from crispy_forms import layout
from django import forms
from django.core.exceptions import ValidationError

import validators
from monitoring.choices import symptom_choices, tests_choices
from prediction.models import HealthCenter
from . import choices


class StatusReportForm(forms.Form):
    report_type = forms.ChoiceField(label='Tipo de relatório', choices=choices.report_type_choices,
                                    widget=forms.Select)
    health_center = forms.ModelChoiceField(label='Unidade de saúde', queryset=HealthCenter.objects.filter(active=True),
                                           required=True, empty_label='Todas')
    period_begin = forms.DateField(label='Data inicial', widget=forms.DateInput(attrs={'type': 'date'}), required=False,
                                   validators=[validators.prevent_past_date, validators.prevent_future_date])
    period_end = forms.DateField(label='Data final', widget=forms.DateInput(attrs={'type': 'date'}), required=False,
                                 validators=[validators.prevent_past_date, validators.prevent_future_date])
    status = forms.ChoiceField(choices=choices.status_choices, required=False, widget=forms.Select)
    test = forms.ChoiceField(label='Tipo de teste', choices=(('', 'Qualquer um'), *tests_choices[:-1]), required=False,
                             widget=forms.Select())
    o2_saturation = forms.FloatField(label='Saturação do oxigênio máxima (%)', min_value=0, max_value=100, required=False)
    address_type = forms.ChoiceField(label='Tipo de endereço', choices=choices.address_type_choices, required=False)
    symptoms = forms.MultipleChoiceField(label='Sintomas reportados', choices=symptom_choices, required=False,
                                         widget=forms.CheckboxSelectMultiple())
    limit = forms.IntegerField(label='Limitar resultados', min_value=1, widget=forms.NumberInput(attrs={'value': ''}),
                               required=False)
    order_by = forms.ChoiceField(label='Ordenar por', choices=choices.order_by_choices, required=False)

    def __init__(self, *args, **kwargs):
        super(StatusReportForm, self).__init__(*args, **kwargs)

        self.helper = helper.FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(layout.Submit(name='', value='Filtrar'))
        self.helper.add_input(layout.Button(css_id='button_id_export', name='', value='Exportar planilha'))

    def clean_limit(self):
        try:
            limit = self.cleaned_data['limit']
            if limit is None:
                return ''
            return int(limit)
        except (ValueError, KeyError):
            raise ValidationError('Limite inválido')

    def clean_address_type(self):
        address_type = self.cleaned_data['address_type']

        if address_type not in {t[0] for t in choices.address_type_choices}:
            raise ValidationError('Tipo de endereço inválido')

        return address_type

    def clean(self):
        cleaned_data = super(StatusReportForm, self).clean()

        period_end = cleaned_data['period_end'] if 'period_end' in cleaned_data else None
        period_begin = cleaned_data['period_begin'] if 'period_begin' in cleaned_data else None

        if period_begin is not None and period_end is not None and period_end < period_begin:
            self.add_error('period_end', 'A data final não pode ser anterior à data inicial')

        return cleaned_data
