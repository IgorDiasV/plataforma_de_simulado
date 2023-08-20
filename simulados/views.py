from django.shortcuts import render, redirect, get_object_or_404
from pagina_principal.models import Questao, Assunto
from .models import Simulado, SimuladoCompartilhado
from .models import RespostaSimulado, RespostaQuestaoSimulado
from random import sample
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.contrib import messages
from django.http.response import Http404
from django.urls import reverse
from utils.utils import qtd_perguntas, qtd_acertos, formatar_tempo
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.utils import lista_questoes


def simulado(request):
    simulado_id = request.POST['simulado_id']
    simulado = get_object_or_404(Simulado, id=simulado_id)
    questoes = simulado.questoes.all()

    return render(request, 'simulados/simulado.html',
                  {'questoes': questoes,
                   'simulado': simulado,
                   'tempo_de_prova': ''})


def gerar_link(request):
    if request.method == 'POST':
        qtd_tentativas = 0
        tempo_de_prova = 0
        if request.POST.get('limite_de_tentativas'):
            qtd_tentativas = obter_valor_ou_zero(request,
                                                 ['qtd_tentativas'])[0]
        if request.POST.get('tempo_limite'):
            campos = ['horas', 'minutos', 'segundos']
            horas, minutos, segundos = obter_valor_ou_zero(request,
                                                           campos)
            tempo_de_prova = horas*3600 + minutos*60 + segundos

        id_simulado = request.POST['id_simulado']
        simulado = Simulado.objects.filter(id=id_simulado).first()
        SimuladoCompartilhado.objects.create(simulado=simulado,
                                             tempo_de_prova=tempo_de_prova,
                                             qtd_tentativas=qtd_tentativas)

        return redirect('simulados:lista_simulados')
    else:
        return Http404()


@login_required(login_url='usuarios:login', redirect_field_name='next')
def dados_simulado(request, simulado_link):
    respostas_simulado = RespostaSimulado.objects.filter(simulado_respondido__link=simulado_link)   # noqa: E501
    usuario = Usuario.objects.filter(user=request.user).first()
    qtd_respostas = len(respostas_simulado.filter(usuario=usuario))
    simulado_compartilhado = get_object_or_404(SimuladoCompartilhado,
                                               link=simulado_link)
    tempo_de_prova = simulado_compartilhado.tempo_de_prova
    tempo_formatado = "Sem Tempo limite"
    if tempo_de_prova > 0:
        tempo_formatado = formatar_tempo(tempo_de_prova)

    qtd_tentativas = simulado_compartilhado.qtd_tentativas

    if qtd_tentativas == 0:
        qtd_tentativas = "Sem limite de tentativas"
    else:
        qtd_tentativas -= qtd_respostas

    simulado = simulado_compartilhado.simulado
    titulo = simulado.titulo
    qtd_questoes = len(simulado.questoes.all())
    professor = simulado.autor.user
    nome_professor = professor.first_name + " " + professor.last_name

    return render(request, 'simulados/dados_simulado.html',
                  {'titulo': titulo,
                   'professor': nome_professor,
                   'qtd_questoes': qtd_questoes,
                   'link': simulado_link,
                   'tempo_de_prova': tempo_formatado,
                   'qtd_tentativas': qtd_tentativas
                   })


@login_required(login_url='usuarios:login', redirect_field_name='next')
def responder_simulado(request):

    if request.method == 'POST':
        link = request.POST['link']
        if not request.session.get('inicio_simulado', None):
            request.session['inicio_simulado'] = datetime.now().ctime()
        inicio_simulado = request.session.get('inicio_simulado', None)

        simulado_compartilhado = get_object_or_404(SimuladoCompartilhado,
                                                   link=link)

        tempo_de_prova = simulado_compartilhado.tempo_de_prova
        simulado = simulado_compartilhado.simulado
        questoes = simulado.questoes.all()

        return render(request, 'simulados/simulado.html',
                      {'questoes': questoes,
                       'simulado': simulado,
                       'link': link,
                       'inicio_simulado': inicio_simulado,
                       'tempo_de_prova': tempo_de_prova
                       })
    else:
        return Http404()


@login_required(login_url='usuarios:login', redirect_field_name='next')
def salvar_resposta(request):
    link = ""
    dados_questoes = []
    for name, value in request.POST.items():
        if name == "link":
            link = value
        elif name != 'csrfmiddlewaretoken':
            aux = {}
            aux['id_questao'] = name
            aux['resposta'] = value
            dados_questoes.append(aux)

    simulado_compartilhado = get_object_or_404(SimuladoCompartilhado,
                                               link=link)

    usuario = Usuario.objects.filter(user=request.user).first()
    resposta_simulado = RespostaSimulado.objects.create(
                                    simulado_respondido=simulado_compartilhado,
                                    usuario=usuario
                                    )
    for dado_questao in dados_questoes:
        id_questao = int(dado_questao['id_questao'])
        questao = get_object_or_404(Questao, id=id_questao)
        resposta = dado_questao['resposta']
        RespostaQuestaoSimulado.objects.create(resposta_simulado=resposta_simulado,  # noqa: E501
                                               questao=questao,
                                               resposta=resposta)
    messages.success(request, "Respotas Salva")
    del (request.session['inicio_simulado'])
    return redirect('home')


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
        
        simulado_respondido = RespostaSimulado.objects.filter(id=id)
        simulado_respondido = simulado_respondido.first().simulado_respondido
        questoes_simulados = simulado_respondido.simulado.questoes.all()
        
        dados_questao = []
        for questao in questoes_simulados:
            resposta_questao = respostas_questoes.filter(questao=questao)
            print(resposta_questao)
            classe = ''
            key = ''
            if len(resposta_questao) > 0:
                resposta_questao = resposta_questao.first()
                classe = "wrong_answer"
                if resposta_questao.resposta == resposta_questao.questao.alternativa_correta:  # noqa: E501
                    classe = "right_answer"
                key = f'classe_alternativa_{resposta_questao.resposta.lower()}'
            dados_questao.append({'questao': questao,
                                 key: classe})   # noqa: E501
            
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
                            f"{reverse('simulados:dados_simulado', args=[link])}"  # noqa: E501
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


def obter_valor_ou_zero(request, campos):
    valores = []
    for campo in campos:
        valor = request.POST.get(campo)
        if valor is None or valor == '':
            valores.append(0)
        else:
            valores.append(int(valor))
    return valores


@login_required(login_url='usuarios:login', redirect_field_name='next')
def criar_simulado_manualmente(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        if request.method == 'POST':
            titulo = request.POST['titulo']
            id_questoes_escolhidas = request.POST.getlist('questoes_escolhidas')  # noqa: E501
            questoes_escolhidas = Questao.objects.all().filter(id__in=id_questoes_escolhidas)  # noqa: E501
            simulado = Simulado.objects.create(titulo=titulo, autor=usuario)  # noqa: E501
            simulado.questoes.set(questoes_escolhidas)
            messages.success(request, 'Simulado Criado com Sucesso')
            return redirect('simulados:lista_simulados')

        assuntos_ids = request.GET.get('id_assuntos_filtro', '')
        anos_ids = request.GET.get('id_anos_filtro', '')

        titulo = request.GET.get('titulo', '')
        id_questoes_escolhidas = request.GET.get('id_questao', '')
        n_pagina = request.GET.get('page', '1')

        questoes_escolhidas = ''
        if assuntos_ids != '':
            assuntos_ids = assuntos_ids.split(",")
        else:
            assuntos_ids = []

        if anos_ids != '':
            anos_ids = anos_ids.split(",")
        else:
            anos_ids = []

        if id_questoes_escolhidas != '':
            id_questoes_escolhidas = id_questoes_escolhidas.split(",")
            questoes_escolhidas = Questao.objects.all().filter(id__in=id_questoes_escolhidas)  # noqa: E501
        else:
            id_questoes_escolhidas = []

        questoes, assuntos, anos = lista_questoes(filtro_assunto=assuntos_ids,
                                                  anos=anos_ids)
        page = ''
        questoes_paginacao = Paginator(questoes, 5)
        try:
            page = questoes_paginacao.page(n_pagina)
        except (EmptyPage, PageNotAnInteger):
            page = questoes_paginacao.page(1)

        return render(request, 'simulados/criar_simulado_manualmente.html',  # noqa: E501
                      {'questoes': page,
                       'assuntos': assuntos,
                       'id_questoes_escolhidas': id_questoes_escolhidas,
                       'questoes_escolhidas': questoes_escolhidas,
                       'titulo': titulo,
                       'id_filtro_assunto': assuntos_ids,
                       'anos_questoes': anos})

    else:
        mensagem = ('Seu perfil é de aluno, '
                    'Apenas professores podem criar simulados')
        messages.error(request, mensagem)
        return redirect('home')


@login_required(login_url='usuarios:login', redirect_field_name='next')
def editar_simulado(request, id):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        if request.method == 'POST':
            assuntos_ids = []
            simulado = Simulado.objects.filter(id=id).first()
            titulo = simulado.titulo

            questoes_escolhidas = simulado.questoes.all()
            id_questoes_escolhidas = [questao.id for questao in questoes_escolhidas]  # noqa: E501

            questoes, assuntos, anos = lista_questoes()
            page = ''
            questoes_paginacao = Paginator(questoes, 5)

            page = questoes_paginacao.page(1)

            return render(request, 'simulados/editar_simulado.html',  # noqa: E501
                          {
                           'id_simulado': id,
                           'questoes': page,
                           'assuntos': assuntos,
                           'id_questoes_escolhidas': id_questoes_escolhidas,
                           'questoes_escolhidas': questoes_escolhidas,
                           'titulo': titulo,
                           'id_filtro_assunto': assuntos_ids,
                           'anos_questoes': anos})
        else:
            assuntos_ids = request.GET.get('id_assuntos_filtro', '')
            anos_ids = request.GET.get('id_anos_filtro', '')

            titulo = request.GET.get('titulo', '')
            id_questoes_escolhidas = request.GET.get('id_questao', '')
            n_pagina = request.GET.get('page', '1')

            questoes_escolhidas = ''
            if assuntos_ids != '':
                assuntos_ids = assuntos_ids.split(",")
            else:
                assuntos_ids = []

            if anos_ids != '':
                anos_ids = anos_ids.split(",")
            else:
                anos_ids = []

            if id_questoes_escolhidas != '':
                id_questoes_escolhidas = id_questoes_escolhidas.split(",")
                questoes_escolhidas = Questao.objects.all().filter(id__in=id_questoes_escolhidas)  # noqa: E501
            else:
                id_questoes_escolhidas = []

            questoes, assuntos, anos = lista_questoes(filtro_assunto=assuntos_ids,  # noqa: E501
                                                      anos=anos_ids)
            page = ''
            questoes_paginacao = Paginator(questoes, 5)
            try:
                page = questoes_paginacao.page(n_pagina)
            except (EmptyPage, PageNotAnInteger):
                page = questoes_paginacao.page(1)

            return render(request, 'simulados/editar_simulado.html',  # noqa: E501
                          {
                           'id_simulado': id,
                           'questoes': page,
                           'assuntos': assuntos,
                           'id_questoes_escolhidas': id_questoes_escolhidas,
                           'questoes_escolhidas': questoes_escolhidas,
                           'titulo': titulo,
                           'id_filtro_assunto': assuntos_ids,
                           'anos_questoes': anos})


def save_edit(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        if request.method == 'POST':
            id_simulado = request.POST['id_simulado']
            titulo = request.POST['titulo']
            id_questoes_escolhidas = request.POST.getlist('questoes_escolhidas')  # noqa: E501
            questoes_escolhidas = Questao.objects.all().filter(id__in=id_questoes_escolhidas)  # noqa: E501
            simulado = Simulado.objects.filter(id=id_simulado).first()  # noqa: E501
            simulado.titulo = titulo
            simulado.questoes.set(questoes_escolhidas)
            simulado.save()
            messages.success(request, 'Simulado Editado com Sucesso')
            return redirect('simulados:lista_simulados')