from django.contrib import messages
from django.contrib.auth import mixins
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, reverse
from django.views import generic
from django.views import View

from django.shortcuts import get_object_or_404, render

from smc19 import settings
from . import forms
from . import models
from monitoring import utils

class SignUp(generic.CreateView):
    template_name = 'sign-up.html'

    def get_form(self, form_class=None):
        if self.request.POST:
            return forms.AccountCreationForm(self.request.user, self.request.POST)
        else:
            return forms.AccountCreationForm(self.request.user)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(SignUp, self).form_invalid(form)

    def form_valid(self, form):
        # Aqui é feita outras validações que não são possíveis no form.clean()
        user = self.request.user
        user_profile = form.cleaned_data['user_profile']
        health_center = form.cleaned_data['health_center']
        if user.user_profile == 'AU':
            # atendente de uma unidade tentou criar um usuário
            messages.error(self.request, "Você não tem permissão para criar outros usuários.")
        elif (user.user_profile == 'AD') and (user_profile == 'SS'):
            # tentou criar um perfil Secretaria de saude
            messages.error(self.request, "Você não pode criar esse tipo de usuário.")
        elif (user.user_profile == 'AD') and (health_center != user.health_center):
            # tentou criar usuário de outra unidade
            messages.error(self.request, "Você não pode criar usuários de outras unidades.")
        elif (user.user_profile == 'SS') and (health_center.group != user.group):
            # tentou criar um usuário de uma unidade pertencente a outro grupo
            messages.error(self.request, 'Você não pode criar usuários em unidades de outros grupos.')
        else:
            new_user = form.save(commit=False)
            new_user.first_login = True
            new_user.group = user.group
            new_user.save()
            messages.success(self.request, "Usuário criado com sucesso.")

        return redirect('accounts:sign-up')


class AccountPasswordChangeView(mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'change_password.html'
    form_class = forms.PasswordChangeForm

    def form_valid(self, form):
        self.request.user.first_login = False
        self.request.user.save()
        return super(AccountPasswordChangeView, self).form_valid(form)


from django.core import paginator


class GroupAccountListView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Account
    template_name = 'accounts/group_users.html'

    def get_context_data(self, **kwargs):
        active_page = self.request.GET.get('active_page')
        inactive_page = self.request.GET.get('inactive_page')

        context = super().get_context_data(**kwargs)

        if self.request.user.user_profile == 'AU':
            group_users = models.Account.objects.none()
        else:
            group_users = models.Account.objects.filter(group=self.request.user.group).exclude(id=self.request.user.id)
            group_users = group_users.exclude(user_profile='SS')

            if self.request.user.user_profile == 'AD':
                group_users = group_users.exclude(user_profile='AD').filter(health_center=self.request.user.health_center)

        context['active_group_users_paginator'] = paginator.Paginator(group_users.filter(is_active=True), 10)
        context['active_group_users'] = context['active_group_users_paginator'].page(active_page)
        context['inactive_group_users_paginator'] = paginator.Paginator(group_users.filter(is_active=False), 10)
        context['inactive_group_users'] = context['inactive_group_users_paginator'].page(inactive_page)

        context['active_page_number'] = active_page
        context['inactive_page_number'] = inactive_page

        return context


class UpdateAccountStateView(mixins.LoginRequiredMixin, View):

    def post(self, request):
        checked_ids = list(self.request.POST.keys())
        checked_ids.remove('csrfmiddlewaretoken')

        for checked_id in checked_ids:
            account = models.Account.objects.get(id=checked_id.split('-')[1])
            account.is_active = not account.is_active
            account.save()

        return redirect(reverse('accounts:list-group-users') + '?active_page=1&inactive_page=1')


class ResetUserPassword(mixins.LoginRequiredMixin, View):
    model = models.Account
    form_class = forms.SetPasswordForm
    template_name = 'password_reset.html'

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(self.model, pk=kwargs['user_id'], group=request.user.group)
        form = self.form_class(user, request.POST)
        if form.is_valid():
            user = form.save()
            user.first_login = True
            user.save()
            messages.success(request, 'A senha do usuário foi resetada !')
            utils.create_log(self.request, 'U', user, "Um secretário de saúde resetou a senha deste usuário")
            return redirect('/accounts/list-group-users/?active_page=1&inactive_page=1')
        else:
            messages.error(request, 'Por favor corrija os erros')
            return render(request, self.template_name, context={'form':form})

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(self.model, pk=kwargs['user_id'])
        form = self.form_class(user)
        return render(request, self.template_name, context={'form':form})