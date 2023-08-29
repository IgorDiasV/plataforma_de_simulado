from django.urls import path
from . import views

app_name = 'simulados'
urlpatterns = [

    path('simulado/dados_simulado/<uuid:simulado_link>/',
         views.dados_simulado, name='dados_simulado'),
    path('simulado/responder_simulado/',
         views.responder_simulado, name='responder_simulado'),
    path('simulado/salvar_resposta/', views.salvar_resposta,
         name='salvar_resposta'),
    path('simulado/respostas_do_simulado/', views.respostas_do_simulado,
         name='respostas_do_simulado'),
    path('simulado/gerar_link/', views.gerar_link, name='gerar_link'),
    path('simulado/criar_simulado_manualmente/save/<str:tipo>',
         views.save, name='save'),
    path('criar_simulado_manualmente/<str:tipo>/',
         views.criar_simulado_manualmente, name='criar_simulado_manualmente'),
    path('simulado/', views.simulado, name='simulado'),
    path('lista_simulado/', views.lista_simulados, name='lista_simulados'),
    path('criar_simulado/', views.criar_simulado, name='criar_simulado'),
    path('resposta_aluno/', views.resposta_aluno, name='resposta_aluno'),
]
