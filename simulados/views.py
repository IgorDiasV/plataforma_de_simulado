from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from pagina_principal.models import Questao, Assunto
from .models import Simulado, SimuladoCompartilhado
import json
from random import sample
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.contrib import messages
from django.http.response import Http404
from django.urls import reverse


def simulado(request):
    simulado_id = request.POST['simulado_id']
    simulado = get_object_or_404(Simulado, id=simulado_id)
    questoes = simulado.questoes.all()

    return render(request, 'simulados/simulado.html',
                  {'questoes': questoes, 'simulado': simulado})


def gerar_link(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        id_simulado = dados['id_simulado']
        simulado = Simulado.objects.filter(id=id_simulado).first()
        simulado_compartilhado = SimuladoCompartilhado.objects.create(simulado=simulado)  # noqa: E501
        link = str(simulado_compartilhado.link)
        link = (f"{request.scheme}://"
                f"{request.get_host()}"
                f"{request.get_full_path()}"
                f"{link}"
                )
        link = str(link)
        print(link)
        return HttpResponse(json.dumps({'link': link}))
    else:
        return Http404()


def responder_simulado(request):
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


@login_required(login_url='usuarios:login', redirect_field_name='next')
def lista_simulados(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    simulados = Simulado.objects.filter(autor=usuario)
    simulados_e_link = []
    for simulado in simulados:
        simulado_compartilhado = SimuladoCompartilhado.objects.filter(simulado=simulado).first()
        aux={}
        aux['simulado'] = simulado
        if simulado_compartilhado is not None:
            link = simulado_compartilhado.link
            url_completa = (f"{request.scheme}://"
                            f"{request.get_host()}"
                            f"{request.get_full_path()}"
                            f"{link}"
                            )
            aux['link'] = url_completa
        simulados_e_link.append(aux)

    return render(request, 'simulados/lista_simulados.html',
                  {'simulados': simulados_e_link})


@login_required(login_url='usuarios:login', redirect_field_name='next')
def criar_simulado(request):
    # TODO Verificar se todos os campos foram preenchidos para evitar erros
    # TODO adicionar requerid no form
    # TODO verificar se a quantiade de questões disponiveis é suficiente
    # para criar o simulado ex: foi pedido para criar um simulado
    # com 10 questões, mas só tem 5 questões cadastradas
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        assuntos = Assunto.objects.all()
        if request.method == 'POST':
            questoes = Questao.objects.all()

            titulo = request.POST['titulo']
            assuntos_ids = request.POST.getlist('assuntos')
            qtd_questoes = int(request.POST['qtd_questoes'])

            if len(assuntos_ids) != 0:
                questoes = questoes.filter(assuntos__id__in=assuntos_ids).distinct()  # noqa: E501

            indices_para_sorteio = list(range(0, len(questoes)))
            indices_escolhidos = sample(indices_para_sorteio, qtd_questoes)
            simulado = Simulado.objects.create(titulo=titulo, autor=usuario)
            for indice in indices_escolhidos:
                simulado.questoes.add(questoes[indice])
            return redirect('simulados:lista_simulados')
        return render(request, 'simulados/criar_simulado.html',
                      {'assuntos': assuntos})
    else:
        mensagem = ('Seu perfil é de aluno, '
                    'Apenas professores podem criar simulados')
        messages.error(request, mensagem)
        return redirect('home')


@login_required(login_url='usuarios:login', redirect_field_name='next')
def criar_simulado_manualmente(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        questoes = Questao.objects.all()
        assuntos = Assunto.objects.all()
        if request.method == 'POST':
            titulo = request.POST['titulo']
            id_questoes_escolhidas = request.POST.getlist('questoes_escolhidas')  # noqa: E501
            questoes_escolhidas = questoes.filter(id__in=id_questoes_escolhidas)  # noqa: E501
            simulado = Simulado.objects.create(titulo=titulo, autor=usuario)
            simulado.questoes.set(questoes_escolhidas)
        return render(request, 'simulados/criar_simulado_manualmente.html',  # noqa: E501
                      {'questoes': questoes, 'assuntos': assuntos})

    else:
        mensagem = ('Seu perfil é de aluno, '
                    'Apenas professores podem criar simulados')
        messages.error(request, mensagem)
        return redirect('home')
