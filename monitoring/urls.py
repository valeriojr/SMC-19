from django.urls import path

from . import views

app_name = 'monitoring'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('mapa/', views.Map.as_view(), name='map'),
    #path('mapa/municipios', views.CitiesList.as_view(), name='cities_list'),
    # Profile
    path('pacientes/<str:term>/buscar', views.ProfileSearch.as_view(), name='profile-search'),
    path('unidades/<str:healthcenter_term>/buscar', views.HealthCenterSearch.as_view(), name='healthcenter-search'),
    path('pacientes/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('pacientes/cadastrar/', views.ProfileCreate.as_view(), name='profile-create'),
    path('pacientes/<int:pk>/editar/', views.ProfileUpdate.as_view(), name='profile-update'),
    path('pacientes/<int:pk>/remover/', views.ProfileDelete.as_view(), name='profile-delete'),
    path('pacientes/<int:pk>/adicionar-familiar/', views.ProfileMakeFamiliar.as_view(), name='make-familiar'),
    path('pacientes/<int:pk>/remover-familiar/<int:familiar_pk>', views.ProfileUnmakeFamiliar.as_view(), name='unmake-familiar'),
    path('pacientes/<int:pk>/registrar-obito/', views.ProfileRegisterDeath.as_view(), name='update-death-date'),
    # Address
    path('pacientes/<int:profile>/enderecos/cadastrar/', views.AddressCreate.as_view(), name='address-create'),
    path('pacientes/<int:profile>/enderecos/<int:pk>/editar/', views.AddressUpdate.as_view(), name='address-update'),
    path('pacientes/<int:profile>/enderecos/<int:pk>/remover/', views.AddressDelete.as_view(), name='address-delete'),
    # Trip
    path('pacientes/<int:profile>/viagens/cadastrar/', views.TripCreate.as_view(), name='trip-create'),
    path('pacientes/<int:profile>/viagens/<int:pk>/editar/', views.TripUpdate.as_view(), name='trip-update'),
    path('pacientes/<int:profile>/viagens/<int:pk>/remover/', views.TripDelete.as_view(), name='trip-delete'),
    # Monitoring
    path('atendimentos/<int:pk>/', views.MonitoringDetail.as_view(), name='monitoring-detail'),
    path('atendimentos/cadastrar/', views.MonitoringCreate.as_view(), name='monitoring-create'),
    path('atendimentos/<int:pk>/editar/', views.MonitoringUpdate.as_view(), name='monitoring-update'),
    path('atendimentos/<int:pk>/remover/', views.MonitoringDelete.as_view(), name='monitoring-delete'),
    # Request
    path('request/', views.RequestIndex.as_view(), name='request'),
    path('request/cadastrar/', views.RequestCreate.as_view(), name='request-create'),
    path('request/<int:pk>/remover/', views.RequestDelete.as_view(), name='request-delete'),
    # Social isolation report
    path('relatorio-isolamento/', views.SocialIsolationReport.as_view(), name='isolation-report'),
    path('listar-municipios/', views.CountyList.as_view(), name='county-list'),
    path('listar-bairros/', views.NeighbourhoodList.as_view(), name='neighbourhood-list'),
    path('pacientes/<int:pk>/relatorio-de-isolamento/', views.IndividualReport.as_view(), name='timeline'),
    # Internações
    path('pacientes/<int:profile>/internacoes/cadastrar/', views.HospitalizationCreate.as_view(), name='hospitalization-create'),
    path('pacientes/<int:profile>/internacoes/<int:pk>/editar/', views.HospitalizationUpdate.as_view(), name='hospitalization-update'),
    path('pacientes/<int:profile>/internacoes/<int:pk>/remover/', views.HospitalizationDelete.as_view(), name='hospitalization-delete'),
    # Contatos
    path('pacientes/<int:profile>/contatos/cadastrar/', views.ContactCreate.as_view(), name='contact-create'),
    path('pacientes/<int:profile>/contatos/<int:pk>/remover/', views.ContactDelete.as_view(), name='contact-delete'),
    # Vacinação
    path('pacientes/<int:profile>/vacinacao/cadastrar/', views.VaccinationCreate.as_view(), name='vaccination-create'),
    path('pacientes/<int:profile>/vacinacao/<int:pk>/editar/', views.VaccinationUpdate.as_view(), name='vaccination-update'),
    path('pacientes/<int:profile>/vacinacao/<int:pk>/remover/', views.VaccinationDelete.as_view(), name='vaccination-delete'),
]
