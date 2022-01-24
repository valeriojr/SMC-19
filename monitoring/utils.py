from datetime import timedelta, date

from .models import ActionLog
from monitoring.models import Profile


def create_log(request, action, content_object, additional_info=''):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    user = request.user
    ActionLog.objects.create(action=action, user=user, ip=ip, content_object=content_object,
                             additional_info=additional_info)


def date_flow(profile, monitoring, diff_attendance_symptom=4):
    """
    Dados um paciente e um atendimento específico, atualiza as datas do paciente baseado no atendimento.
    """
    three_days = timedelta(days=3)
    fourteen_days = timedelta(days=14)

    if monitoring.symptom_set.count() > 0:
        profile.fill_first_symptoms_date()
    else:
        profile.fill_estimated_first_symptoms_date(diff_attendance_symptom)

    # Checagem 1: O paciente precisa ter exclusivamente a data dos primeiros sintomas ou a data estimada do primeiro sintoma
    if profile.first_symptom_onset is None and profile.estimated_first_symptom is None:
        raise Exception('O paciente precisa ter a data do primeiro sintoma ou a data estimada do primeiro sintoma.')
    if profile.first_symptom_onset is not None and profile.estimated_first_symptom is not None:
        raise Exception('O paciente pode ter apenas data do primeiro sintoma ou a data estimada do primeiro sintoma.')

    # Confirmado / Recuperado
    if monitoring.is_confirmed() or profile.is_confirmed():
        # verifica se o atendimento tem orientacao para monitoramento
        check_monitored(profile, monitoring)

        # Se ja eh confirmado, atualiza data de recuperacao
        if profile.is_confirmed():
            profile.recovered_date = max(profile.recovered_date,
                                         monitoring.attendance_date + three_days,
                                         (profile.monitored_date or date(1900, 1, 1)))
        # define data de confirmacao e recuperacao caso contrario
        else:
            profile.confirmed_date = monitoring.attendance_date
            recover_date = profile.first_symptom_onset or profile.estimated_first_symptom
            profile.recovered_date = max(monitoring.attendance_date + three_days,
                                         recover_date + fourteen_days,
                                         (profile.monitored_date or date(1900, 1, 1)))

        # Checagem 2: O paciente precisa ter a data de confirmação e a data de recuperação
        if profile.confirmed_date is None or profile.recovered_date is None:
            raise Exception('O paciente precisa ter a data de confirmação e a data de recuperação')

    # Suspeito / Descartado
    elif profile.is_suspect():
        # Atualiza a data de descarte
        profile.discarded_date = max(profile.discarded_date, monitoring.attendance_date + three_days)

        # Checagem 3: O paciente precisa ter a data de suspeito e a data de descarte
        if profile.suspect_date is None or profile.discarded_date is None:
            raise Exception('O paciente precisa ter a data de suspeito e a data de descarte')
    else:
        if monitoring.is_suspect():
            profile.suspect_date = monitoring.attendance_date
            discard_date = profile.first_symptom_onset or profile.estimated_first_symptom
            profile.discarded_date = max(monitoring.attendance_date + three_days, discard_date + fourteen_days)

            # Checagem 3: O paciente precisa ter a data de suspeito e a data de descarte
            if profile.suspect_date is None or profile.discarded_date is None:
                raise Exception('O paciente precisa ter a data de suspeito e a data de descarte')

    # Checagem 4: Se tem data de monitorado então tem data de confirmado e tem data de recuperado
    if (profile.monitored_date is not None) and ((profile.confirmed_date is None) or (profile.recovered_date is None)):
        raise Exception('O paciente precisa ter data de confirmação e data de \
                recuperação caso tenha data do fim do monitoramento.')

    # Se tem data de confirmado, então deve ter recuperado e vice-versa
    if ( (profile.confirmed_date is not None) and (profile.recovered_date is None) ) \
       or ( (profile.confirmed_date is None) and (profile.recovered_date is not None) ):
        raise Exception('O paciente precisa ter data de recuperação e de confirmação simultaneamente.')

    # Se tem data de suspeito, então deve ter descartado e vice-versa
    if ( (profile.suspect_date is not None) and (profile.discarded_date is None) ) \
       or ( (profile.suspect_date is None) and (profile.discarded_date is not None) ):
        raise Exception('O paciente precisa ter data de descarte e de suspeita simultaneamente.')


def check_monitored(profile, monitoring):
    # casos monitorado sao casos confirmados com encaminhamento para isolamento em casa
    if (monitoring.is_confirmed() or profile.is_confirmed()) and monitoring.is_monitored():
        monitored_period = timedelta(days=monitoring.medical_referral_duration)
        if profile.monitored_date is None:
            monitored_date = date(1900, 1, 1)
        else:
            monitored_date = profile.monitored_date
        # fim do monitoramento
        profile.monitored_date = max(monitored_date, monitoring.attendance_date + monitored_period)


def mean_diff_attendance_symptom():
    profiles = Profile.objects.all()

    means = []
    for p in profiles:
        monitorings = p.monitoring_set.all()
        if monitorings.count() == 0:
            continue

        profile_sum = 0
        for m in monitorings:
            if m.symptom_set.count() == 0:
                 continue

            diff = abs((m.symptom_set.first().onset - m.attendance_date).days)
            # diferenças maiores que 15 são prossivelmente erro no cadastro
            if diff > 15:
                continue
            profile_sum += diff

        means.append(profile_sum / monitorings.count())

    final_mean = round(sum(means) / profiles.count())
    print("Media das diferenças entre atendimento e primeiro sintoma: ", final_mean)

    return final_mean
