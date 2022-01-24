from django.urls import path

from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('confirmed-cases/', views.CasesPerStatus.as_view(), name='confirmed-cases'),
    path('<str:group>/informe-epidemiologico/', views.EpidemiologicalReport.as_view(), name='epidemiologic-report')
]
