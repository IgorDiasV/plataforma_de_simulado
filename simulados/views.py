from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from pagina_principal.models import Questao, Assunto
from .models import Simulado, SimuladoCompartilhado
from .models import RespostaSimulado, RespostaQuestaoSimulado
import json
from random import sample
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.contrib import messages
from django.http.response import Http404
from django.urls import reverse
from utils.utils import qtd_perguntas, qtd_acertos


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
                f"{reverse('simulados:responder_simulado', args=[link])}"
                )
        link = str(link)
        return HttpResponse(json.dumps({'link': link}))
    else:
        return Http404()


@login_required(login_url='usuarios:login', redirect_field_name='next')
def responder_simulado(request, simulado_link):
    simulado = get_object_or_404(SimuladoCompartilhado,
                                 link=simulado_link).simulado
    questoes = simulado.questoes.all()

    return render(request, 'simulados/simulado.html',
                  {'questoes': questoes,
                   'simulado': simulado,
                   'link': simulado_link})


@login_required(login_url='usuarios:login', redirect_field_name='next')
def salvar_resposta(request):
    dados = json.loads(request.body)
    link = dados['link']
    dados_questoes = dados['questoes']
    simulado_compartilhado = get_object_or_404(SimuladoCompartilhado,
                                               link=link)

    usuario = Usuario.objects.filter(user=request.user).first()
    resposta_simulado = RespostaSimulado.objects.create(
                                    simulado_respondido=simulado_compartilhado,
                                    usuario=usuario
                                    )
    for dado_questao in dados_questoes:
        id_questao = int(dados_questoes[dado_questao]['id_questao'])
        questao = get_object_or_404(Questao, id=id_questao)
        resposta = dados_questoes[dado_questao]['resposta']
        RespostaQuestaoSimulado.objects.create(resposta_simulado=resposta_simulado,  # noqa: E501
                                               questao=questao,
                                               resposta=resposta)

    return HttpResponse('1')


@login_required(login_url='usuarios:login', redirect_field_name='next')
def respostas_do_simulado(request):
    if request.method == 'POST':
        id_simulado = request.POST['id_simulado']
        respostas = RespostaSimulado.objects.filter(simulado_respondido__simulado__id=id_simulado)   # noqa: E501
        qtd_perguntas_simulado = qtd_perguntas(id_simulado)
        alunos_que_responderam = []
        for resposta in respostas:
            qtd_acertos_aluno = qtd_acertos(resposta.id)
            desempenho = f'{qtd_acertos_aluno}/{qtd_perguntas_simulado}'
            nome = f'{resposta.usuario.user.first_name} {resposta.usuario.user.last_name}'   # noqa: E501
            email = resposta.usuario.user.email
            alunos_que_responderam.append({'id_resposta': resposta.id,
                                           'nome': nome,
                                           'email': email,
                                           'desempenho': desempenho})

        return render(request, 'simulados/respostas_do_simulado.html',
                      {'alunos': alunos_que_responderam})
    else:
        return Http404()


@login_required(login_url='usuarios:login', redirect_field_name='next')
def resposta_aluno(request):
    if request.method == 'POST':
        id = request.POST['id_resposta']
        respostas_questoes = RespostaQuestaoSimulado.objects.filter(resposta_simulado__id=id)  # noqa: E501

        dados_questao = []

        for resposta_questao in respostas_questoes:

            classe = "wrong_answer"
            if resposta_questao.resposta == resposta_questao.questao.alternativa_correta:  # noqa: E501
                classe = "right_answer"

            dados_questao.append({'questao': resposta_questao.questao,
                                  f'classe_alternativa_{resposta_questao.resposta.lower()}': classe})   # noqa: E501

        return render(request, 'simulados/exibir_resultado.html',
                      {'dados_questoes': dados_questao})
    else:
        return Http404()


@login_required(login_url='usuarios:login', redirect_field_name='next')
def lista_simulados(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    simulados = Simulado.objects.filter(autor=usuario)
    simulados_e_link = []

    for simulado in simulados:
        simulado_compartilhado = SimuladoCompartilhado.objects.filter(simulado=simulado).first()   # noqa: E501
        aux = {}
        aux['simulado'] = simulado

        if simulado_compartilhado is not None:
            link = simulado_compartilhado.link
            url_completa = (f"{request.scheme}://"
                            f"{request.get_host()}"
                            f"{reverse('simulados:responder_simulado', args=[link])}"  # noqa: E501
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
