from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('change-password/', views.AccountPasswordChangeView.as_view(), name='change-password'),
    path('list-group-users/', views.GroupAccountListView.as_view(), name='list-group-users'),
    path('update-accounts-status/', views.UpdateAccountStateView.as_view(), name='update-account-status'),
    path('reset-user-password/<int:user_id>/', views.ResetUserPassword.as_view(), name='reset-user-password')
]