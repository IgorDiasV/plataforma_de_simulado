from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def criar_simulado(request):
    return render(request, 'criar_simulado.html')

def buscar_questoes(request):
    return render(request, 'buscar_questoes.html')

