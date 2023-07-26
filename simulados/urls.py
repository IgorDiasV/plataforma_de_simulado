from django.urls import path
from . import views

app_name = 'simulados'
urlpatterns = [
    path('simulado/<int:simulado_id>', views.simulado, name='simulado'),
    path('lista_simulado/', views.lista_simulados, name='lista_simulados'),
    path('criar_simulado/', views.criar_simulado, name='criar_simulado'),
    path('criar_simulado_manualmente/',
         views.criar_simulado_manualmente, name='criar_simulado_manualmente')
]
