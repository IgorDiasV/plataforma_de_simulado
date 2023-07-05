from django.urls import path
from . import  views
urlpatterns = [
    path('', views.home, name='home'),
    path('lista_questoes/', views.lista_questoes, name='lista_questoes'),
    path('cadastrar_questao/', views.cadastrar_questao, name='cadastrar_questao'),
    path('editar_questao/<int:questao_id>/', views.editar_questao, name='editar_questao'),
    path('simulado', views.simulado, name='simulado')
]
