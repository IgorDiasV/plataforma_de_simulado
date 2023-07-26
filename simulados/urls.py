from django.urls import path
from . import views

app_name = 'simulados'
urlpatterns = [
    path('simulado/', views.simulado, name='simulado'),
    path('simulado/responder_simulado/<uuid:simulado_link>/',
         views.responder_simulado, name='responder_simulado'),
    path('resposta_do_simulado/', views.resposta_do_simulado,
         name='resposta_do_simulado'),
    path('simulado/gerar_link/', views.gerar_link, name='gerar_link'),
    path('lista_simulado/', views.lista_simulados, name='lista_simulados'),
    path('criar_simulado/', views.criar_simulado, name='criar_simulado'),
    path('criar_simulado_manualmente/',
         views.criar_simulado_manualmente, name='criar_simulado_manualmente')
]
