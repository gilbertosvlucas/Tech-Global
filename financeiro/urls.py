from django.urls import path
from . import views

urlpatterns = [
    path('receber/', views.lista_contas_receber, name='lista_contas_receber'),
    path('receber/nova/', views.nova_conta_receber, name='nova_conta_receber'),
    path('pagar/', views.lista_contas_pagar, name='lista_contas_pagar'),
    path('pagar/nova/', views.nova_conta_pagar, name='nova_conta_pagar'),

]
