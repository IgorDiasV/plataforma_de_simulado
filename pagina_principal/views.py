from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Questao, Assunto, Simulado
import json
from random import sample


def home(request):
    return render(request, 'pagina_principal/home.html')


def lista_questoes(request):
    questoes = Questao.objects.all()
    assuntos = Assunto.objects.all()

    if request.method == 'POST':
        assuntos_ids = request.POST.getlist('assuntos')       
        if len(assuntos_ids) != 0:
            questoes = questoes.filter(assuntos__id__in=assuntos_ids)

    return render(request, 'pagina_principal/lista_questoes.html',
                  {'questoes': questoes, 'assuntos': assuntos})


def simulado(request, simulado_id):

    simulado = get_object_or_404(Simulado, id=simulado_id)
    questoes = simulado.questoes.all()
    if request.method == 'POST':
        dados = json.loads(request.body)
        resposta = []
        for questao in dados: 
            dados_questao = get_object_or_404(Questao, 
                                              id=dados[questao]['id_questao'])

            if dados_questao.alternativa_correta == dados[questao]['resposta']:
                resposta.append({'status': 'Resposta Correta',
                                 'id_questao': dados[questao]['id_questao']})
            else:
                resposta.append({'status': 'Resposta Errada',
                                 'id_questao': dados[questao]['id_questao']})
        return HttpResponse(json.dumps({'resultado': resposta}))
    
    return render(request, 'pagina_principal/simulado.html',
                  {'questoes': questoes, 'simulado': simulado})


def cadastrar_questao(request):
    assuntos = Assunto.objects.all()
    if request.method == 'POST':
        dados = json.loads(request.body)
        assuntos_ids = dados['assuntos']
        questao = Questao.objects.create(pergunta=dados['pergunta'], 
                                         curso=dados['nome_curso'],  
                                         alternativa_a=dados['alternativa_a'], 
                                         alternativa_b=dados['alternativa_b'],
                                         alternativa_c=dados['alternativa_c'],
                                         alternativa_d=dados['alternativa_d'],
                                         alternativa_e=dados['alternativa_e'],
                                         alternativa_correta=dados['alternativa_correta']  # noqa: E501
                                         )

        assuntos_aux = assuntos_ids.copy()
        for assunto_pagina in assuntos_aux:
            if 'novo_' in assunto_pagina:
                assuntos_ids.remove(assunto_pagina)
                assunto_pagina = assunto_pagina.replace('novo_', '')
                assunto_novo = Assunto.objects.create(nome_assunto=assunto_pagina)  # noqa: E501
                questao.assuntos.add(assunto_novo)

        assuntos_ids = list(map(int, assuntos_ids))
        assuntos = Assunto.objects.filter(id__in=assuntos_ids)
        for assunto in assuntos: 
            questao.assuntos.add(assunto)

    return render(request, 'pagina_principal/cadastrar_questao.html',
                  {'assuntos': assuntos})


def editar_questao(request, questao_id):
    
    questao = get_object_or_404(Questao, id=questao_id)

    if request.method == 'POST':
        dados = json.loads(request.body)
        questao.pergunta = dados['pergunta']
        questao.curso = dados['nome_curso']
        questao.alternativa_a = dados['alternativa_a']
        questao.alternativa_b = dados['alternativa_b']
        questao.alternativa_c = dados['alternativa_c']
        questao.alternativa_d = dados['alternativa_d']
        questao.alternativa_e = dados['alternativa_e']
        questao.alternativa_correta = dados['alternativa_correta']

        questao.save()
        
        return HttpResponse('1')
            
    return render(request, 'pagina_principal/editar_questao.html', 
                  {'questao': questao})


def criar_simulado(request):
    # TODO Verificar se todos os campos foram preenchidos para evitar erros
    # TODO adicionar requerid no form
    # TODO verificar se a quantiade de questões disponiveis é suficiente
    # para criar o simulado ex: foi pedido para criar um simulado
    # com 10 questões, mas só tem 5 questões cadastradas

    assuntos = Assunto.objects.all()
    if request.method == 'POST':
        questoes = Questao.objects.all()

        titulo = request.POST['titulo']
        assuntos_ids = request.POST.getlist('assuntos')
        qtd_questoes = int(request.POST['qtd_questoes'])
        
        if len(assuntos_ids) != 0:
            questoes = questoes.filter(assuntos__id__in=assuntos_ids).distinct()
        
        indices_para_sorteio = list(range(0, len(questoes)))
        indices_escolhidos = sample(indices_para_sorteio, qtd_questoes)
        simulado = Simulado.objects.create(titulo=titulo)
        for indice in indices_escolhidos:
            simulado.questoes.add(questoes[indice])
        return redirect('lista_simulados')
    return render(request, 'pagina_principal/criar_simulado.html', 
                  {'assuntos': assuntos})


def criar_simulado_manualmente(request):
    questoes = Questao.objects.all()
    assuntos = Assunto.objects.all()
    if request.method == 'POST':
        titulo = request.POST['titulo']
        id_questoes_escolhidas = request.POST.getlist('questoes_escolhidas')
        questoes_escolhidas = questoes.filter(id__in=id_questoes_escolhidas)
        simulado = Simulado.objects.create(titulo=titulo)
        simulado.questoes.set(questoes_escolhidas)
    return render(request, 'pagina_principal/criar_simulado_manualmente.html',
                  {'questoes': questoes, 'assuntos': assuntos})


def lista_simulados(request):
    simulados = Simulado.objects.all()
    return render(request, 'pagina_principal/lista_simulados.html',
                  {'simulados': simulados})


