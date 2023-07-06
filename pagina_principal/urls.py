from django.urls import path
from . import  views
urlpatterns = [
    path('', views.home, name='home'),
    path('lista_questoes/', views.lista_questoes, name='lista_questoes'),
    path('cadastrar_questao/', views.cadastrar_questao, name='cadastrar_questao'),
    path('editar_questao/<int:questao_id>/', views.editar_questao, name='editar_questao'),
    path('simulado/<int:simulado_id>', views.simulado, name='simulado'),
    path('lista_simulado/', views.lista_simulados, name='lista_simulados'),
    path('criar_simulado/', views.criar_simulado, name='criar_simulado'),
    # path('teste_simulado/<int:simulado_id>', views.teste_simulado, name='teste_simulado')
]
