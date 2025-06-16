from django.urls import path
from . import views

urlpatterns = [
    path('orcamentos/', views.lista_orcamentos, name='lista_orcamentos'),
    path('orcamentos/novo/', views.novo_orcamento, name='novo_orcamento'),
    path('orcamentos/<int:orcamento_id>/editar/', views.editar_orcamento, name='editar_orcamento'),
    path('orcamentos/<int:orcamento_id>/excluir/', views.excluir_orcamento, name='excluir_orcamento'),
  
]

