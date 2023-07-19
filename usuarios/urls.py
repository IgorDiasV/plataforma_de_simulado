from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('', views.login, name='login')
    
]
