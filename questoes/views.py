from django.shortcuts import render, redirect, get_object_or_404
from .models import Questao, Assunto
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.contrib import messages
from utils.utils import assuntos_removidos, assuntos_adicionados
from utils.utils import lista_questoes, get_parametros_url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'questoes/home.html')


@login_required(login_url='usuarios:login', redirect_field_name='next')
def lista_questoes_geral(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        lista_parametros = ['id_assuntos_filtro',
                            'id_anos_filtro'
                            ]
        valores_parametros = get_parametros_url(request, lista_parametros)

        anos = valores_parametros['id_anos_filtro']
        assuntos_ids = valores_parametros['id_assuntos_filtro']
        
        dados_questoes = lista_questoes(filtro_assunto=assuntos_ids,
                                        anos=anos,
                                        )

        questoes = dados_questoes['questoes']
        assuntos = dados_questoes['assuntos']
        anos_questoes = dados_questoes['anos_questoes']

        page = ''
        n_pagina = request.GET.get('page', '1')
        questoes_paginacao = Paginator(questoes, 5)
        try:
            page = questoes_paginacao.page(n_pagina)
        except (EmptyPage, PageNotAnInteger):
            page = questoes_paginacao.page(1)

        return render(request, 'questoes/lista_questoes.html',
                      {'questoes': page,
                       'assuntos': assuntos,
                       'anos_questoes': anos_questoes,
                       'id_filtro_assunto': assuntos_ids,
                       'anos_filtro': anos, })
    else:
        mensagem = ('Seu perfil é de aluno, '
                    'apenas professores têm acesso a listagem de questões ')
        messages.error(request, mensagem)
        return redirect('home')


@login_required(login_url='usuarios:login', redirect_field_name='next')
def lista_questoes_usuario(request):
    usuario = Usuario.objects.filter(user=request.user).first()

    lista_parametros = ['id_assuntos_filtro',
                        'id_anos_filtro',
                        ]
    valores_parametros = get_parametros_url(request, lista_parametros)

    anos = valores_parametros['id_anos_filtro']
    assuntos_ids = valores_parametros['id_assuntos_filtro']

    dados_questoes = lista_questoes(usuario=usuario,
                                    filtro_assunto=assuntos_ids,
                                    anos=anos,
                                    )

    questoes = dados_questoes['questoes']
    assuntos = dados_questoes['assuntos']
    anos_questoes = dados_questoes['anos_questoes']

    page = ''
    n_pagina = request.GET.get('page', '1')
    questoes_paginacao = Paginator(questoes, 5)
    try:
        page = questoes_paginacao.page(n_pagina)
    except (EmptyPage, PageNotAnInteger):
        page = questoes_paginacao.page(1)

    return render(request, 'questoes/lista_questoes.html',
                  {'questoes': page, 'assuntos': assuntos,
                   'editavel': True,
                   'anos_questoes': anos_questoes,
                   'id_filtro_assunto': assuntos_ids,
                   'anos_filtro': anos,
                   })


@login_required(login_url='usuarios:login', redirect_field_name='next')
def cadastrar_questao(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        assuntos = Assunto.objects.all()
        if request.method == 'POST':
            nome_curso = request.POST['nome_curso']
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

        return render(request, 'questoes/cadastrar_questao.html',
                      {'assuntos': assuntos})
    else:
        mensagem = ('Seu perfil é de aluno, '
                    'Apenas professores podem cadastrar questões')
        messages.error(request, mensagem)
        return redirect('home')


@login_required(login_url='usuarios:login', redirect_field_name='next')
def editar_questao(request, questao_id):

    questao = get_object_or_404(Questao, id=questao_id)
    usuario = Usuario.objects.filter(user=request.user).first()
    assuntos_geral = Assunto.objects.all()
    
    assuntos_questao = questao.assuntos.all()
    assuntos_selecionados = [str(assunto.id) for assunto in assuntos_questao]

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

        return render(request, 'questoes/editar_questao.html',
                      {'questao': questao,
                       'assuntos': assuntos_geral,
                       'assuntos_selecionados': assuntos_selecionados})
    else:
        mensagem = ('Apenas o autor dessa questão pode altera-la')
        messages.error(request, mensagem)
        return redirect('home')
