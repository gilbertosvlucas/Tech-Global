from django.urls import path
from . import views

urlpatterns = [
    path('receber/', views.lista_contas_receber, name='lista_contas_receber'),
    path('receber/nova/', views.nova_conta_receber, name='nova_conta_receber'),
    path('pagar/', views.lista_contas_pagar, name='lista_contas_pagar'),
    path('pagar/nova/', views.nova_conta_pagar, name='nova_conta_pagar'),
    
    # Contas a Receber
    path('receber/editar/<int:conta_id>/', views.editar_conta_receber, name='editar_conta_receber'),
    path('receber/excluir/<int:conta_id>/', views.excluir_conta_receber, name='excluir_conta_receber'),

    # Contas a Pagar
    path('pagar/editar/<int:conta_id>/', views.editar_conta_pagar, name='editar_conta_pagar'),
    path('pagar/excluir/<int:conta_id>/', views.excluir_conta_pagar, name='excluir_conta_pagar'),

]
