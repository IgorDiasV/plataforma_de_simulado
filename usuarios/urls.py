from django.urls import path
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('cadastro/salvar/', views.salvar_cadastro, name='salvar_cadastro'),
    path('login/', views.login_view, name='login'),
    path('login/realizar_login/', views.realizar_login, name='realizar_login'),
    path('logout/', views.logout_view, name='logout'),
]
