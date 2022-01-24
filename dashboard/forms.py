from datetime import datetime

from django import forms

import validators


class EpidemiologicalReportForm(forms.Form):
    date__lte = forms.DateField(label='Data', initial=datetime.now().date(), required=False,
                                widget=forms.DateInput(attrs={'type': 'date'}),
                                validators=[validators.prevent_future_date])

class DateFilter(forms.Form):
    start_date = forms.DateField(label="Data inicial", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="Data final", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    start_date.widget.attrs.update({"class": "form-control"})
    end_date.widget.attrs.update({"class": "form-control"})