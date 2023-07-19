from django.shortcuts import render
from .forms import  RegisterForm


def cadastro_view(request):
    form = RegisterForm()
    return render(request, 'usuarios/pages/cadastro_view.html', {'form': form})
    
def login(request):
    return render(request, 'usuarios/pages/login.html')
