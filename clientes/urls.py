from django.urls import path
from . import views
from .views_auth import LoginUsuario, LogoutUsuario

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('novo/', views.novo_cliente, name='novo_cliente'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('excluir/<int:cliente_id>/', views.excluir_cliente, name='excluir_cliente'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', LogoutUsuario.as_view(), name='logout'),
    path('<int:cliente_id>/interacoes/', views.listar_interacoes, name='listar_interacoes'),
    path('<int:cliente_id>/interacoes/nova/', views.nova_interacao, name='nova_interacao'),
]
