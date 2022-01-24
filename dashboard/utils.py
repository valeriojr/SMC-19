from datetime import timedelta
import pandas

from django.db.models import Q
from django.utils.timezone import datetime

from monitoring.models import Monitoring, Profile
from mathmodels.python_scripts import mathmodels


def get_previsao_leitos(group):
    monitorings = []
    for i in range(7):
        gte = datetime.now()-timedelta(days=i+1)
        lte = datetime.now()-timedelta(days=i)
        monitorings.append(Monitoring.objects.filter(profile__group_id=group, attendance_date__gte=gte,
                                                     attendance_date__lte=lte))

    ranges = ['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79','80+']
    patients = {_range:[] for _range in ranges}
    monitorings.reverse()

    for _range in ranges:
        for monitoring in monitorings:
            if _range == '80+':
                gte = int(_range.split('+')[0])

                patients[_range].append(len(monitoring.filter(profile__age__gte=gte)))
            else:
                gte = int(_range.split('-')[0])
                lte = int(_range.split('-')[1])

                patients[_range].append(len(monitoring.filter(profile__age__gte=gte, profile__age__lte=lte)))

    return mathmodels.predict_beds_simple(patients, days=4)[1]


def count_daily(group, date):
    count = {
        'suspect': 0,
        'confirmed': 0,
        'monitored': 0,
        'recovered': 0,
        'discarded': 0,
        'deaths': 0,
    }

    for p in Profile.objects.filter(group=group):  #.filter(Q(recovered_date=date) | Q(monitored_date__gte=date) |
                                                   #     Q(death_date=date) | Q(discarded_date=date) |
                                                   #     Q(confirmed_date=date) | Q(suspect_date=date)):
        dates_validation(p)

        if p.death_date:
            if p.death_date == date:
                count['deaths'] += 1
                if p.confirmed_date == date:
                    count['confirmed'] += 1
                continue

            if p.death_date < date:
                continue

        if p.recovered_date == date:
            count['recovered'] += 1
            continue

        if p.monitored_date:
            if p.monitored_date >= date:
                count['monitored'] += 1
                if p.confirmed_date == date:
                    count['confirmed'] += 1
                continue

        if p.confirmed_date == date:
            count['confirmed'] += 1
            continue

        if p.discarded_date == date and p.recovered_date is None:
            count['discarded'] += 1
            continue

        if p.suspect_date == date:
            count['suspect'] += 1
            continue

    return count


def dates_validation(p):
    today = datetime.now().date()
    if p.confirmed_date is not None or p.recovered_date is not None:
        assert p.recovered_date > p.confirmed_date, "recuperacao <= confirmacao: (id: %d)" % (p.id)
    if p.monitored_date is not None:
        assert p.monitored_date > p.confirmed_date, "monitoramento <= confirmacao: (id: %d)" % (p.id)
    if p.suspect_date is not None or p.discarded_date is not None:
        assert p.discarded_date > p.suspect_date, "descarte <= suspeita: (id: %d)" % (p.id)
    if p.confirmed_date is not None:
        assert p.confirmed_date <= today, "confirmacao > hoje: (id: %d)" % (p.id)
    if p.suspect_date is not None:
        assert p.suspect_date <= today, "suspeita > hoje: (id: %d)" % (p.id)
    if p.monitored_date is not None:
        assert p.recovered_date >= p.monitored_date, "recuperacao < monitoramento: (id: %d)" % (p.id)
    if p.confirmed_date is not None and p.suspect_date is not None:
        assert p.confirmed_date >= p.suspect_date, "confirmacao < suspeita: (id: %d)" % (p.id)
    if p.death_date is not None:
        assert p.death_date <= today, "morte > hoje: (id: %s)" % (p.id)

def generate_df_daily_avg(df, column, interval):
    if df.shape[0]>0:
        idx = pandas.date_range(df[column][0], df[column][df.shape[0]-1])
        s = df.set_index(column)['count']
        s.index = pandas.DatetimeIndex(s.index)
        s = s.reindex(idx, fill_value=0)
        df = s.to_frame().reset_index(drop=False).rename(columns={'index': column})
        df[column] = df[column].apply(lambda x: x.strftime("%Y-%m-%d"))
        df['moving_avg'] = df.rolling(window=interval).mean().fillna(0).round(2)

        return df
    else:
        return pandas.DataFrame(columns=[column, 'count', 'moving_avg'])