import json
import os
from datetime import timedelta

import pandas
from django import views
from django.contrib import messages
from django.contrib.auth import mixins
from django.db import connection
from django.db.models import Q
from django.forms import DateInput
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from pyUFbr.baseuf import ufbr
from unidecode import unidecode

from monitoring import choices
from smc19 import settings
import utils
from . import forms
from . import models
from . import utils

from prediction.models import HealthCenter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.

class Index(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Profile
    paginate_by = 5
    template_name = 'monitoring/index.html'

    def get_queryset(self):
        params = dict(zip(self.request.GET.keys(), self.request.GET.values()))

        if params.get('search-target') == 'profile':
            search_term = self.request.GET.get('term')
            return models.Profile.objects.filter(Q(full_name__icontains=search_term) |
                                                 Q(id_document__startswith=search_term) |
                                                 Q(cpf__startswith=search_term) |
                                                 Q(cns__startswith=search_term))
        else:
            # retorna todos os profiles que não é familiar de ninguém
            return models.Profile.objects.filter(Q(group_id=self.request.user.group)).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)

        context['params'] = self.request.GET
        context['monitorings'] = models.Monitoring.objects.filter(Q(health_center_id__group=self.request.user.group)
                                                                 ).order_by('-created')[:10]
        context['monitoring_create_form'] = forms.MonitoringForm()
        symptoms_initial = [{'symptom': symptom[0], 'label': symptom[1]} for symptom in choices.symptom_choices]
        context['symptom_formset'] = forms.SymptomInlineFormset(initial=symptoms_initial)

        return context


# nao eh mais necessario
# cross site funcionando no gcloud
# class CitiesList(mixins.LoginRequiredMixin, generic.base.View):
#    def get(self, request, *args, **kwargs):
#        with open('static/data/municipios.json') as json_file:
#            data = json.load(json_file)
#        return JsonResponse(data, safe=False)


class Map(mixins.LoginRequiredMixin, generic.FormView):
    template_name = 'monitoring/map.html'
    form_class = forms.MapForm

    def get_form(self, form_class=None):
        return self.form_class(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super(Map, self).get_context_data(**kwargs)

        form = self.get_form()

        if form.is_valid():
            df = pandas.read_excel(
                os.path.join(settings.STATICFILES_DIRS[0], 'data/map/paciente_01_06_2020_alagoas.xlsx'))

            if form.cleaned_data['classification'] == 'confirmado':
                date = 'data_atendimento'
            elif form.cleaned_data['classification'] == 'obito':
                date = 'data_obito'

            df = df[df.classificacao.str.lower() == 'confirmado']
            if form.cleaned_data['classification'] == 'obito':
                df = df[df.situacao_atual.str.lower() == 'óbito'].dropna(subset=['data_obito'])

            # Pré-processamento
            df.municipio_residencia = df.municipio_residencia.apply(lambda m: unidecode(m).upper())
            county_list = df.municipio_residencia.unique()
            df[date] = df[date].apply(lambda d: d.split('T')[0])
            # Agrupa os dados pela data do atendimento/data óbito + municipio de residencia

            df = df.groupby([date, 'municipio_residencia']).classificacao.count().to_dict()

            data = {}
            for k, v in df.items():
                if k[0] in data:
                    data[k[0]].update({k[1]: v})
                else:
                    data[k[0]] = {k[1]: v}

            keys = list(data.keys())

            for i in range(1, len(data)):
                for c in data[keys[i - 1]]:
                    if c in data[keys[i]]:
                        data[keys[i]][c] += data[keys[i - 1]][c]
                    else:
                        data[keys[i]][c] = data[keys[i - 1]][c]

            context['data'] = data
        else:
            context['data'] = {}

        return context

    def form_invalid(self, form):
        print('Form invalid')
        messages.error(self.request, form.errors)
        return super(Map, self).form_invalid(form)


# Profile

class ProfileSearch(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Profile

    def get(self, request, *args, **kwargs):
        search_term = self.kwargs['term']
        profiles = list(models.Profile.objects.filter(Q(full_name__icontains=search_term) |
                                                      Q(id_document__startswith=search_term) |
                                                      Q(cpf__startswith=search_term) |
                                                      Q(cns__startswith=search_term)).values())
        return JsonResponse(profiles, safe=False)


class ProfileCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.ProfileForm
    template_name = 'monitoring/new_profile.html'
    success_url = reverse_lazy('monitoring:index')

    def get_context_data(self, **kwargs):
        context = super(ProfileCreate, self).get_context_data(**kwargs)

        if self.request.POST:
            context['primary_address_form'] = forms.AddressInlineFormset(self.request.POST)
        else:
            context['primary_address_form'] = forms.AddressInlineFormset()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        address_form = context['primary_address_form']

        cpf = form.cleaned_data['cpf']
        birthplace = form.cleaned_data['birthplace']
        # se for estrangeiro, o cpf entra vazio e só assim pode repetir
        if models.Profile.objects.filter(cpf=cpf).count() > 0 and (not birthplace):
            messages.error(self.request, 'Já existe um perfil cadastrado com esse CPF')
            return self.form_invalid(form)

        if address_form.is_valid():
            self.object = form.save(commit=False)
            self.object.group = self.request.user.group
            address_list = address_form.save(commit=False)
            if len(address_list) != 1:
                messages.error(self.request, 'Formulário de endereço inválido')
                return self.form_invalid(form)

            self.object.save()

            address = address_list[0]
            address.profile = self.object
            address.primary = True

            address.save()
            utils.create_log(self.request, 'C', address)
        else:
            print(address_form.errors)
            return self.form_invalid(form)

        utils.create_log(self.request, 'C', self.object)
        return super(ProfileCreate, self).form_valid(form)

    def form_invalid(self, form):
        return super(ProfileCreate, self).form_invalid(form)


class ProfileDetail(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Profile
    template_name = 'monitoring/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)

        monitorings = self.object.monitoring_set.all()

        confirmed = False
        for monitoring in monitorings:
            if monitoring.result == 'PO':
                confirmed = True
                break

        context['confirmed'] = confirmed

        context['update_profile_form'] = forms.ProfileForm(instance=self.object)
        context['address_form'] = forms.AddressForm(data={
            'profile': self.object.id
        })
        context['trip_form'] = forms.TripForm(data={
            'profile': self.object.id
        })

        context['primary_address_form'] = forms.AddressInlineFormset()  # pra o endereço do familiar

        context['hospitalization_form'] = forms.HospitalizationForm(
            data={
                'profile': self.object.id
            }
        )
        context['hospitalization_form'].fields['entry'].required = False
        context['hospitalization_form'].fields['departure'].required = False

        context['contact_form'] = forms.ContactForm(data={
            'profile': self.object.id
        })

        context['vaccination_form'] = forms.VaccinationForm(data={
            'profile': self.object.id
        })

        context['familiars'] = models.Profile.objects.filter(family=self.object.family, family__isnull=False).exclude(
            id=self.object.id)

        comorbidities = []
        for comorbidity in self.object.comorbidities:
            comorbidities.append({
                'label': self.object.comorbidities.get_label(comorbidity[0]),
                'set': comorbidity[1]
            })

        context['comorbidities'] = comorbidities

        return context


class ProfileUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Profile
    form_class = forms.ProfileForm

    def form_valid(self, form):
        messages.success(self.request, 'Paciente atualizado com sucesso!')
        base_model = models.Profile.objects.get(id=self.object.id)
        utils.create_log(self.request, 'U', self.object,
            ', '.join(['{}({})'.format(changed, getattr(base_model, changed)) for changed in form.changed_data]))
        return super(ProfileUpdate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['pk']])


class ProfileUnmakeFamiliar(mixins.LoginRequiredMixin, generic.View):
    def post(self, request, pk, familiar_pk, *args, **kwargs):
        try:
            profile = get_object_or_404(models.Profile, pk=pk)
            other_profile = get_object_or_404(models.Profile, pk=familiar_pk)
            if profile.family == other_profile.family:
                other_profile.family = None
                other_profile.save()
                utils.create_log(
                    self.request, 'U',
                    other_profile,
                    'Familiar teve atributo family alterado para null'
                )
            else:
                messages.error(self.request, 'Não é possível remover um familiar que não é da familia do paciente !')
        except Http404:
            messages.error(self.request, 'Paciente não encontrado!')
        except Exception as e:
            messages.error(self.request, e)

        return HttpResponseRedirect(reverse('monitoring:profile-detail', kwargs={'pk': profile.id}))


class ProfileDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Profile
    success_url = reverse_lazy('monitoring:index')

    def post(self, request, *args, **kwargs):
        profile = self.get_object()

        if request.user.group != profile.group:
            messages.error(self.request, 'Você não possui permissão para realizar esta ação')
            return HttpResponseRedirect(reverse('monitoring:profile-detail', kwargs={'pk': profile.id}))

        utils.create_log(request, 'D', profile)
        return super(ProfileDelete, self).post(request, *args, **kwargs)


class ProfileMakeFamiliar(mixins.LoginRequiredMixin, generic.View):
    def post(self, request, pk, *args, **kwargs):
        other = self.request.POST.get('other')
        try:
            profile = get_object_or_404(models.Profile, pk=pk)
            other_profile = get_object_or_404(models.Profile, pk=other)
            profile.make_familiar(other_profile)
        except Http404:
            messages.error(self.request, 'Paciente não encontrado!')
        except Exception as e:
            messages.error(self.request, e)

        return HttpResponseRedirect(reverse('monitoring:profile-detail', kwargs={'pk': profile.id}))


class ProfileRegisterDeath(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Profile
    fields = ['death_date']
    template_name = 'monitoring/profile_update_death_date.html'

    def get_success_url(self):
        return reverse('monitoring:profile-detail', kwargs={'pk': self.object.id})

    def get_form(self, form_class=None):
        form = super(ProfileRegisterDeath, self).get_form(form_class)
        form.fields['death_date'].widget = DateInput(format='%Y-%m-%d', attrs={'type': 'date'})

        return form

    def form_valid(self, form):
        death_date = models.Profile.objects.get(id=self.object.id).death_date
        utils.create_log(self.request, 'U', self.object, "data do óbito: %s. data anterior: %s" % (self.object.death_date, death_date))
        return super(ProfileRegisterDeath, self).form_valid(form)


# Address

class AddressCreate(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Address
    form_class = forms.AddressForm

    def form_valid(self, form):
        self.object = form.save()
        utils.create_log(self.request, 'C', self.object)
        return super(AddressCreate, self).form_valid(form)

    def form_invalid(self, form):
        errors = ''
        for x in form.visible_fields():
            if x.errors:
                for error in x.errors:
                    messages.error(self.request, "%s: %s" % (x.label, error))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class AddressUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Address
    form_class = forms.AddressForm

    def form_valid(self, form):
        base_model = models.Address.objects.get(id=self.object.id)
        changed_data = form.changed_data
        changed_data.remove('input_text_neighbourhood')
        utils.create_log(self.request, 'U', self.object,
            ', '.join(['{}({})'.format(changed, getattr(base_model, changed)) for changed in form.changed_data]))
        return super(AddressUpdate, self).form_valid(form)

    def form_invalid(self, form):
        errors = ''
        for x in form.visible_fields():
            if x.errors:
                for error in x.errors:
                    messages.error(self.request, "%s: %s" % (x.label, error))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class AddressDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Address

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', self.get_object())
        return super(AddressDelete, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


# Monitoring

class MonitoringDetail(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Monitoring

    def get_context_data(self, **kwargs):
        context = super(MonitoringDetail, self).get_context_data(**kwargs)

        # Formulário de edição do atendimento atual
        context['monitoring_update_form'] = forms.MonitoringForm(instance=self.object)

        symptoms_initial = []
        for symptom in choices.symptom_choices:
            s = models.Symptom.objects.filter(monitoring=self.object, symptom=symptom[0])
            if len(s) > 0:
                symptoms_initial.append({
                    'symptom': symptom[0],
                    'label': symptom[1],
                    'onset': s[0].onset
                })
            else:
                symptoms_initial.append({
                    'symptom': symptom[0],
                    'label': symptom[1]
                })

        context['symptom_formset'] = forms.SymptomInlineFormset(initial=symptoms_initial)

        exposures = []
        for exposure in self.object.virus_exposure:
            exposures.append({
                'label': self.object.virus_exposure.get_label(exposure[0]),
                'set': exposure[1]
            })

        context['exposures'] = exposures

        return context


def symptoms_before_monitoring(symptom_formset, monitoring):
    for symptom in symptom_formset:
        onset = symptom.cleaned_data.get('onset', None)
        if onset is not None and onset > monitoring.attendance_date:
            return False
    return True

class MonitoringCreate(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Monitoring
    form_class = forms.MonitoringForm
    template_name = 'monitoring/monitoring_create.html'

    def get_context_data(self, **kwargs):
        context = super(MonitoringCreate, self).get_context_data(**kwargs)

        symptoms_initial = [{'symptom': symptom[0], 'label': symptom[1]} for symptom in choices.symptom_choices]

        if self.request.POST:
            context['symptom_formset'] = forms.SymptomInlineFormset(self.request.POST, initial=symptoms_initial)
        else:
            context['symptom_formset'] = forms.SymptomInlineFormset(initial=symptoms_initial)

        context['monitoring_create_form'] = context['form']

        #   context['hospitalization_create_form'] = forms.HospitalizationForm()

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        symptom_formset = context['symptom_formset']

        if symptom_formset.is_valid():
            self.object = form.save(commit=False)
            if self.object.profile.death_date is not None:
                messages.error(self.request,
                               'Não é possível cadastrar um atendimento para um paciente que já entrou em óbitos')
                return self.form_invalid(form)
            if not symptoms_before_monitoring(symptom_formset, self.object):
                    messages.error(self.request,
                                   'A data de surgimento dos sintomas deve ser anterior à do atendimento')
                    return self.form_invalid(form)

            self.object.health_center = self.request.user.health_center
            self.object.created_by = self.request.user

            self.object.save()

            for formset in symptom_formset:
                instance = formset.save(commit=False)
                if instance.onset is not None:
                    if self.object.profile.first_symptom_onset is None:
                        self.object.profile.first_symptom_onset = instance.onset
                    else:
                        self.object.profile.first_symptom_onset = min(self.object.profile.first_symptom_onset,
                                                                      instance.onset)
                    instance.monitoring = self.object
                    instance.save()
                    utils.create_log(self.request, 'C', instance)

            self.object.calculate_score()
            self.object.save()

            run_date_flow(self.object.profile, self.request)

            #   Esconde o formulário que cria internação 
            #
            #   hospitalization_form = forms.HospitalizationForm(self.request.POST)
            #   if hospitalization_form.is_valid():
            #       hospitalization_form.save()
            #       messages.success(self.request, 'Internação adicionada com sucesso!')

            messages.success(self.request, 'Atendimento cadastrado com sucesso!')

            utils.create_log(self.request, 'C', self.object)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(MonitoringCreate, self).form_invalid(form)

    def get_success_url(self):
        return reverse('monitoring:index')


class MonitoringUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Monitoring
    form_class = forms.MonitoringForm

    def get_context_data(self, **kwargs):
        context = super(MonitoringUpdate, self).get_context_data(**kwargs)

        if self.request.POST:
            symptoms_initial = [{'symptom': symptom[0], 'label': symptom[1]} for symptom in choices.symptom_choices]
            context['symptom_formset'] = forms.SymptomInlineFormset(self.request.POST, initial=symptoms_initial)

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        symptom_formset = context['symptom_formset']

        if symptom_formset.is_valid():
            self.object = form.save(commit=False)

            if self.request.user.group != self.object.health_center.group:
                messages.error(self.request, 'Você não possui permissão para realizar esta ação')
                return HttpResponseRedirect(reverse('monitoring:monitoring-detail', kwargs={'pk': self.object.id}))
            if not symptoms_before_monitoring(symptom_formset, self.object):
                    messages.error(self.request,
                                   'A data de surgimento dos sintomas deve ser anterior à do atendimento')
                    return self.form_invalid(form)

            for formset in symptom_formset:
                instance = formset.save(commit=False)
                symptoms = self.object.symptom_set.filter(symptom=instance.symptom)
                if len(symptoms) == 1:
                    if instance.onset is not None:
                        if instance.onset != symptoms[0].onset:  # Checa se o sintoma foi alterado
                            symptoms[0].onset = instance.onset
                            symptoms[0].save()
                            utils.create_log(self.request, 'U', symptoms[0], additional_info='Data do surgimento')
                    else:
                        utils.create_log(self.request, 'D', symptoms[0])
                        symptoms[0].delete()
                else:
                    if instance.onset is not None:
                        instance.monitoring = self.object
                        instance.save()
                        utils.create_log(self.request, 'C', instance)

            self.object.calculate_score()

            base_model = models.Monitoring.objects.get(id=self.object.id)
            self.object.save()
            utils.create_log(self.request, 'U', self.object,
                ', '.join(['{}({})'.format(changed, getattr(base_model, changed)) for changed in form.changed_data]))

            run_date_flow(self.object.profile, self.request)

            messages.success(self.request, 'Atendimento atualizado com sucesso!')

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:monitoring-detail', args=[self.kwargs['pk']])


class MonitoringDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Monitoring

    def post(self, request, *args, **kwargs):
        monitoring = self.get_object()
        profile = monitoring.profile

        if request.user.group != monitoring.health_center.group:
            messages.error(self.request, 'Você não tem permissão para realizar esta ação')
            return HttpResponseRedirect(reverse('monitoring:monitoring-detail', kwargs={'pk': monitoring.id}))

        utils.create_log(request, 'D', monitoring)
        monitoring.delete()

        run_date_flow(profile, self.request)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:index')


# Trip

class TripCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.TripForm

    def form_valid(self, form):
        self.object = form.save()
        utils.create_log(self.request, 'C', self.object)
        return super(TripCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class TripUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Trip
    form_class = forms.TripForm

    def form_valid(self, form):
        base_model = models.Trip.objects.get(id=self.object.id)
        utils.create_log(self.request, 'U', self.object,
            ', '.join(['{}({})'.format(changed, getattr(base_model, changed)) for changed in form.changed_data]))
        return super(TripUpdate, self).form_valid(form)
    
    def form_invalid(self, form):
        errors = ''
        for x in form.visible_fields():
            if x.errors:
                for error in x.errors:
                    messages.error(self.request, "%s: %s" % (x.label, error))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class TripDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Trip

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', self.get_object())
        return super(TripDelete, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class RequestCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.RequestForm
    template_name = 'monitoring/new_request.html'
    success_url = reverse_lazy('monitoring:request')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        utils.create_log(self.request, 'C', self.object)
        return HttpResponseRedirect(self.success_url)


class RequestIndex(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'monitoring/request_index.html'
    context_object_name = 'all_requests'

    def get_queryset(self):
        return models.Request.objects.all()


class RequestDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Request
    success_url = reverse_lazy('monitoring:request')

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', self.get_object())
        return super(RequestDelete, self).post(request, *args, **kwargs)


class SocialIsolationReport(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'monitoring/social_isolation_report.html'
    filters = ['medical_referral', 'medical_referral_status']

    def get_context_data(self, **kwargs):
        context = super(SocialIsolationReport, self).get_context_data(**kwargs)

        sql_query = '''
        SELECT
            monitoring_profile.*,
            last_monitorings.*
        FROM 
            monitoring_profile 
            JOIN 
                (
                SELECT 
                    monitoring_monitoring.*,
                    MAX(monitoring_monitoring.created) AS latest_date 
                FROM
                    monitoring_monitoring 
                GROUP BY
                    monitoring_monitoring.profile_id
                ) last_monitorings
            ON 
                monitoring_profile.id = last_monitorings.profile_id
            JOIN 
                monitoring_address
            ON
                monitoring_profile.id = monitoring_address.profile_id 
        WHERE 
            monitoring_address.`primary` = 1
            AND CURRENT_DATE BETWEEN last_monitorings.created 
                AND DATE(last_monitorings.created, '+'||last_monitorings.medical_referral_duration||' days')
                 
        '''

        params = []

        for filter in self.request.GET.keys():
            if filter.split('__')[0] not in self.filters:
                continue
            try:
                sql_query += ' AND %s %s %%s ' % (filter, self.get_operator(filter))
            except KeyError:
                # print('KeyError')
                return HttpResponseForbidden()

            params.append(self.request.GET[filter])

        with connection.cursor() as cursor:
            cursor.execute(sql_query, params)
            context['profile_list'] = utils.dictfetchall(cursor)

        context['filters'] = forms.SocialIsolationReportForm()

        return context

    def get_operator(self, filter):
        operators = {
            filter: '=',
            'lt': '<',
            'gt': '>',
            'lte': '<=',
            'gte': '>=',
            'ne': '!=',
        }

        operator = filter.split('__')[-1]

        if operator in operators:
            return operators[operator]
        else:
            raise KeyError()


class CountyList(views.View):
    def get(self, request):
        return HttpResponse(json.dumps(ufbr.list_cidades(sigla=request.GET.get('uf', ''))))


class NeighbourhoodList(views.View):
    def get(self, request):
        with open(os.path.join(BASE_DIR,'static/data/bairros.json'), 'r', encoding='utf-8') as json_file:
            bairros = json.load(json_file)
        return HttpResponse(json.dumps(bairros.get(request.GET.get('city', ''), {})))


class IndividualReport(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Profile
    template_name = 'monitoring/individual_report.html'

    def get_context_data(self, **kwargs):
        context = super(IndividualReport, self).get_context_data(**kwargs)

        timeline = []

        for monitoring in self.object.monitoring_set.all():
            timeline.append({
                'date': monitoring.created,
                'event': 'Atendimento',
                'description': monitoring.get_description()
            })

        for trip in self.object.trip_set.all():
            timeline.append({
                'date': trip.departure_date,
                'event': 'Viagem',
                'description': 'Viajou para %s-%s' % (trip.county, trip.state),
            })
            timeline.append({
                'date': trip.return_date,
                'event': 'Viagem',
                'description': 'Retornou da viagem'
            })

        context['timeline'] = timeline

        return context


class HealthCenterSearch(mixins.LoginRequiredMixin, generic.CreateView):
    def get(self, request, *args, **kwargs):
        search_term = self.kwargs['healthcenter_term']
        healthcenters = list(HealthCenter.objects.filter(Q(center_name__icontains=search_term) |
                                                      Q(ibge_code__startswith=search_term) |
                                                      Q(cnes_code__startswith=search_term) |
                                                      Q(postal_code__startswith=search_term)).values())
        return JsonResponse(healthcenters, safe=False)


class HospitalizationCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.HospitalizationForm

    def form_valid(self, form):
        self.object = form.save()
        utils.create_log(self.request, 'C', self.object)
        return super(HospitalizationCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class HospitalizationUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Hospitalization
    form_class = forms.HospitalizationForm

    def form_valid(self, form):
        base_model = models.Hospitalization.objects.get(id=self.object.id)
        utils.create_log(self.request, 'U', self.object,
            ', '.join(['{}({})'.format(changed, getattr(base_model, changed)) for changed in form.changed_data]))
        #utils.create_log(self.request, 'U', self.object, additional_info=', '.join(form.changed_data))
        return super(HospitalizationUpdate, self).form_valid(form)

    def form_invalid(self, form):
        errors = ''
        for x in form.visible_fields():
            if x.errors:
                for error in x.errors:
                    messages.error(self.request, "%s: %s" % (x.label, error))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class HospitalizationDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Hospitalization

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', self.get_object())
        return super(HospitalizationDelete, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class ContactCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.ContactForm

    def form_valid(self, form):
        self.object = form.save()
        utils.create_log(self.request, 'C', self.object)
        return super(ContactCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class ContactDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Contact

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', self.get_object())
        return super(ContactDelete, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


def run_date_flow(profile, request):
    # guarda datas antigas no log antes de resetar
    old_dates = "confirmado: %s, recuperado: %s, suspeito: %s, descartado: %s, monitorado: %s, primeiro sintoma: %s, primeiro sintoma estimado: %s" % \
        (profile.confirmed_date, profile.recovered_date, profile.suspect_date, profile.discarded_date, profile.monitored_date, profile.first_symptom_onset, profile.estimated_first_symptom)
    utils.create_log(request, 'U', profile, additional_info=old_dates)

    # reinicia as datas do paciente, exceto morte
    profile.first_symptom_onset = None
    profile.estimated_first_symptom = None
    profile.confirmed_date = None
    profile.recovered_date = None
    profile.suspect_date = None
    profile.discarded_date = None
    profile.monitored_date = None

    # recalcula datas usando todos os atendimentos do paciente
    for m in profile.monitoring_set.order_by('attendance_date'):
        # usando estimativa padrão para estimativa de primeiro sintoma
        utils.date_flow(profile, m)
    profile.save()


class VaccinationCreate(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.VaccinationForm

    def form_valid(self, form):
        self.object = form.save()
        utils.create_log(self.request, 'C', self.object)
        return super(VaccinationCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class VaccinationUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Vaccination
    form_class = forms.VaccinationForm

    def form_valid(self, form):
        base_model = models.Vaccination.objects.get(id=self.object.id)
        utils.create_log(self.request, 'U', self.object,
            ', '.join(['{}({})'.format(changed, getattr(base_model, changed)) for changed in form.changed_data]))
        return super(VaccinationUpdate, self).form_valid(form)

    def form_invalid(self, form):
        errors = ''
        for x in form.visible_fields():
            if x.errors:
                for error in x.errors:
                    messages.error(self.request, "%s: %s" % (x.label, error))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])


class VaccinationDelete(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Vaccination

    def post(self, request, *args, **kwargs):
        utils.create_log(request, 'D', self.get_object())
        return super(VaccinationDelete, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('monitoring:profile-detail', args=[self.kwargs['profile']])
