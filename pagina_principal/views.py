from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Questao, Assunto
import json

def home(request):
    return render(request, 'home.html')

def lista_questoes(request):
    questoes = Questao.objects.all()
    assuntos = Assunto.objects.all()

    if request.method == 'POST':
        assuntos_ids = request.POST.getlist('assuntos')
        tipo_questao = request.POST['tipo_questao']
        
        if len(assuntos_ids) != 0:
            questoes = questoes.filter(assuntos__id__in=assuntos_ids)

        if tipo_questao != '':
            questoes = questoes.filter(tipo_questao=tipo_questao)

    return render(request, 'lista_questoes.html', {'questoes':questoes, 'assuntos':assuntos})

def simulado(request):
    questoes = Questao.objects.all()
    if request.method == 'POST':
        dados = json.loads(request.body)
        resposta = []
        for questao in dados: 
            dados_questao = get_object_or_404(Questao, id = dados[questao]['id_questao'])

            if dados_questao.alternativa_correta == dados[questao]['resposta']:

                resposta.append({'status':'Resposta Correta', 'id_questao':dados[questao]['id_questao']})
            else:
                resposta.append({'status':'Resposta Errada', 'id_questao':dados[questao]['id_questao']})
        return HttpResponse(json.dumps({'resultado':resposta}))
        
    
    return render(request,'simulado.html', {'questoes':questoes})

def cadastrar_questao(request):
    assuntos = Assunto.objects.all()
    if request.method == 'POST':
        dados = json.loads(request.body)
        assuntos_ids = dados['assuntos']
        questao = Questao.objects.create( pergunta = dados['pergunta'], curso = dados['nome_curso'], tipo_questao = dados['tipo_questao'],
                n_questao = dados['n_questao'], alternativa_a = dados['alternativa_a'], alternativa_b = dados['alternativa_b'],
                alternativa_c = dados['alternativa_c'], alternativa_d = dados['alternativa_d'], alternativa_e = dados['alternativa_e'],
                alternativa_correta = dados['alternativa_correta'] )

        assuntos_aux = assuntos_ids.copy()
        for assunto_pagina in assuntos_aux:
            if 'novo_' in assunto_pagina:
                assuntos_ids.remove(assunto_pagina)
                assunto_pagina = assunto_pagina.replace('novo_', '')
                assunto_novo = Assunto.objects.create(nome_assunto=assunto_pagina)         
                questao.assuntos.add(assunto_novo)

        assuntos_ids = list(map(int, assuntos_ids))
        assuntos = Assunto.objects.filter(id__in=assuntos_ids)
        for assunto in assuntos: 
            questao.assuntos.add(assunto)

    return render(request, 'cadastrar_questao.html', {'assuntos':assuntos})

def editar_questao(request, questao_id):
    
    questao = get_object_or_404(Questao, id = questao_id)

    if request.method == 'POST':    
            dados = json.loads(request.body)
            questao.pergunta = dados['pergunta']
            questao.curso = dados['nome_curso']
            questao.tipo_questao = dados['tipo_questao']
            questao.n_questao = dados['n_questao']
            questao.alternativa_a = dados['alternativa_a']
            questao.alternativa_b = dados['alternativa_b']
            questao.alternativa_c = dados['alternativa_c']
            questao.alternativa_d = dados['alternativa_d']
            questao.alternativa_e = dados['alternativa_e']
            questao.alternativa_correta = dados['alternativa_correta']

            questao.save()
            
            return HttpResponse('1')
            
    return render(request, 'editar_questao.html', {'questao': questao})

