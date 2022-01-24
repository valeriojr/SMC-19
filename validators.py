import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_cpf(cpf):
    # verificar o tamanho da string
    if len(cpf) != 11:
        raise ValidationError('O CPF deve conter exatamente 11 dígitos')

    try:
        int(cpf)
    except ValueError:
        raise ValidationError('CPF inválido')

    # cpfs inválidos
    for i in range(10):
        if cpf == str(i) * 11:
            raise ValidationError('CPF inválido')

    # validação do primeiro dígito verificador
    s = 0
    for i in range(9):
        s += int(cpf[i]) * (10 - i)
    first_digit_valid = int(cpf[9]) == ((s * 10 % 11) % 10)

    # validação do segundo dígito verificador
    s = 0
    for i in range(10):
        s += int(cpf[i]) * (11 - i)
    second_digit_valid = int(cpf[10]) == ((s * 10 % 11) % 10)

    if not first_digit_valid or not second_digit_valid:
        raise ValidationError('CPF inválido')


def prevent_future_date(date):
    if date > timezone.now().date():
        raise ValidationError('Data no futuro')


def prevent_past_date(date):
    if date.year < 1900:
        raise ValidationError('A data não pode ser anterior a 1900')


def only_after_2020(date):
    if date.year < 2020:
        raise ValidationError('A data não pode ser anterior a 2020')


def only_after_2021(date):
    if date.year < 2021:
        raise ValidationError('A data não pode ser anterior a 2021')


def validate_cns(cns):
    print('Validating %s' % cns)
    if cns == '' or cns is None:
        return

    def weighted_sum(cns):
        i = 0
        sum = 0
        while i < len(cns):
            sum = sum + int(cns[i]) * (15 - i)
            i = i + 1
        return sum

    if cns.isdigit():
        if re.match(r'[1-2]\d{10}00[0-1]\d$', cns) or re.match(r'[7-9]\d{14}$', cns):
            if weighted_sum(cns) % 11 == 0:
                return

    raise ValidationError('CNS inválido')


def only_digits(string):
    for c in string:
        if c not in '0123456789':
            raise ValidationError('São permitidos apenas números')
