from django.shortcuts import render, redirect, get_object_or_404
from .models import Questao, Assunto
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.contrib import messages
from utils.utils import assuntos_removidos, assuntos_adicionados
from utils.utils import lista_questoes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'pagina_principal/home.html')


def dados_get_lista_questao(request):
    assuntos_ids = request.GET.get('id_assuntos_filtro', '')
    anos = request.GET.get('id_anos_filtro', '')
    n_pagina = request.GET.get('page', '1')

    if assuntos_ids != '':
        assuntos_ids = assuntos_ids.split(",")
    else:
        assuntos_ids = []

    if anos != '':
        anos = anos.split(",")
    else:
        anos = []

    return anos, assuntos_ids, n_pagina


def lista_questoes_geral(request):

    anos, assuntos_ids, n_pagina = dados_get_lista_questao(request)
    questoes, assuntos, anos_questoes = lista_questoes(
                                            filtro_assunto=assuntos_ids,
                                            anos=anos)

    page = ''
    questoes_paginacao = Paginator(questoes, 5)
    try:
        page = questoes_paginacao.page(n_pagina)
    except (EmptyPage, PageNotAnInteger):
        page = questoes_paginacao.page(1)

    return render(request, 'pagina_principal/lista_questoes.html',
                  {'questoes': page,
                   'assuntos': assuntos,
                   'anos_questoes': anos_questoes,
                   'id_filtro_assunto': assuntos_ids,
                   'anos_filtro': anos})


@login_required(login_url='usuarios:login', redirect_field_name='next')
def lista_questoes_usuario(request):
    # TODO falta adicionar a paginação
    usuario = Usuario.objects.filter(user=request.user).first()

    anos, assuntos_ids, n_pagina = dados_get_lista_questao(request)
    questoes, assuntos, anos_questoes = lista_questoes(
                                                usuario=usuario,
                                                filtro_assunto=assuntos_ids,
                                                anos=anos

                                                )
    page = ''
    questoes_paginacao = Paginator(questoes, 2)
    try:
        page = questoes_paginacao.page(n_pagina)
    except (EmptyPage, PageNotAnInteger):
        page = questoes_paginacao.page(1)

    return render(request, 'pagina_principal/lista_questoes.html',
                  {'questoes': page, 'assuntos': assuntos,
                   'editavel': True,
                   'anos_questoes': anos_questoes,
                   'id_filtro_assunto': assuntos_ids,
                   'anos_filtro': anos
                   })


@login_required(login_url='usuarios:login', redirect_field_name='next')
def cadastrar_questao(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        assuntos = Assunto.objects.all()
        if request.method == 'POST':
            nome_curso = request.POST['nome_curso']
            origem = request.POST['origem']
            ano = request.POST['ano']
            assuntos_ids = request.POST.getlist('assuntos')
            pergunta = request.POST['pergunta']
            alternativa_a = request.POST['alternativa_a']
            alternativa_b = request.POST['alternativa_b']
            alternativa_c = request.POST['alternativa_c']
            alternativa_d = request.POST['alternativa_d']
            alternativa_e = request.POST['alternativa_e']
            resposta = request.POST['resposta']
            questao = Questao.objects.create(pergunta=pergunta,
                                             curso=nome_curso,
                                             origem=origem,
                                             ano=ano,
                                             alternativa_a=alternativa_a,
                                             alternativa_b=alternativa_b,
                                             alternativa_c=alternativa_c,
                                             alternativa_d=alternativa_d,
                                             alternativa_e=alternativa_e,
                                             alternativa_correta=resposta,
                                             autor=usuario
                                             )

            assuntos_aux = assuntos_ids.copy()
            for assunto_pagina in assuntos_aux:
                if 'novo_' in assunto_pagina:
                    assuntos_ids.remove(assunto_pagina)
                    assunto_pagina = assunto_pagina.replace('novo_', '')
                    assunto_novo = Assunto.objects.create(nome_assunto=assunto_pagina)  # noqa: E501
                    questao.assuntos.add(assunto_novo)

            assuntos_ids = list(map(int, assuntos_ids))
            assuntos_escolhidos = Assunto.objects.filter(id__in=assuntos_ids)
            for assunto in assuntos_escolhidos:
                questao.assuntos.add(assunto)

            messages.success(request, "Questão Cadastrada com Sucesso")
            return redirect('home')

        return render(request, 'pagina_principal/cadastrar_questao.html',
                      {'assuntos': assuntos})
    else:
        mensagem = ('Seu perfil é de aluno, '
                    'Apenas professores podem cadastrar questões')
        messages.error(request, mensagem)
        return redirect('home')


@login_required(login_url='usuarios:login', redirect_field_name='next')
def editar_questao(request, questao_id):
    # TODO
    # adicionar novos assuntos
    # remover assuntos
    # cadastrar novos assuntos

    questao = get_object_or_404(Questao, id=questao_id)
    usuario = Usuario.objects.filter(user=request.user).first()
    assuntos_geral = Assunto.objects.all()

    assuntos_questao = questao.assuntos.all()
    assuntos = []
    for assunto in assuntos_geral:
        aux = {}

        aux['id'] = assunto.id
        aux['nome_assunto'] = assunto.nome_assunto

        if assunto in assuntos_questao:
            aux['status'] = 'selected'

        assuntos.append(aux)

    if questao.autor == usuario:
        if request.method == 'POST':
            nome_curso = request.POST['nome_curso']
            assuntos_ids = request.POST.getlist('assuntos')

            pergunta = request.POST['pergunta']
            alternativa_a = request.POST['alternativa_a']
            alternativa_b = request.POST['alternativa_b']
            alternativa_c = request.POST['alternativa_c']
            alternativa_d = request.POST['alternativa_d']
            alternativa_e = request.POST['alternativa_e']
            resposta = request.POST['resposta']

            questao.curso = nome_curso
            questao.pergunta = pergunta
            questao.alternativa_a = alternativa_a
            questao.alternativa_b = alternativa_b
            questao.alternativa_c = alternativa_c
            questao.alternativa_d = alternativa_d
            questao.alternativa_e = alternativa_e
            questao.alternativa_correta = resposta

            assuntos_aux = assuntos_ids.copy()
            for assunto_pagina in assuntos_aux:
                if 'novo_' in assunto_pagina:
                    assuntos_ids.remove(assunto_pagina)
                    assunto_pagina = assunto_pagina.replace('novo_', '')
                    assunto_novo = Assunto.objects.create(nome_assunto=assunto_pagina)  # noqa: E501
                    questao.assuntos.add(assunto_novo)

            assuntos_novos = list(map(int, assuntos_ids))
            assuntos_antigos = [assunto_questao.id for assunto_questao in assuntos_questao]  # noqa: E501

            assuntos_para_remover = assuntos_removidos(assuntos_antigos, assuntos_novos)  # noqa: E501
            assuntos_para_adicionar = assuntos_adicionados(assuntos_antigos, assuntos_novos)  # noqa: E501

            for assunto in assuntos_para_remover:
                assunto_removido = Assunto.objects.filter(id=assunto).first()
                questao.assuntos.remove(assunto_removido)

            for assunto in assuntos_para_adicionar:
                assunto_adicionado = Assunto.objects.filter(id=assunto).first()
                questao.assuntos.add(assunto_adicionado)

            questao.save()

            messages.success(request, "questão editada com Sucesso")
            return redirect('home')

        return render(request, 'pagina_principal/editar_questao.html',
                      {'questao': questao, 'assuntos': assuntos})
    else:
        mensagem = ('Apenas o autor dessa questão pode altera-la')
        messages.error(request, mensagem)
        return redirect('home')
