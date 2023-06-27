from django.contrib import admin
from django.urls import path
from . import views

app_name = 'enade'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('buscar_questoes/', views.buscar_questoes, name='buscar_questoes'),
    path('criar_simulado/', views.criar_simulado, name='criar_simulado')
]
