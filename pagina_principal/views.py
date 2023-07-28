from django.shortcuts import render, redirect, get_object_or_404
from .models import Questao, Assunto
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.contrib import messages


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


@login_required(login_url='usuarios:login', redirect_field_name='next')
def lista_questoes_usuario(request):
    assuntos = Assunto.objects.all()
    usuario = Usuario.objects.filter(user=request.user).first()
    questoes = Questao.objects.filter(autor=usuario)

    if request.method == 'POST':
        assuntos_ids = request.POST.getlist('assuntos')
        if len(assuntos_ids) != 0:
            questoes = questoes.filter(assuntos__id__in=assuntos_ids)

    return render(request, 'pagina_principal/lista_questoes.html',
                  {'questoes': questoes, 'assuntos': assuntos,
                   'editavel': True})


@login_required(login_url='usuarios:login', redirect_field_name='next')
def cadastrar_questao(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        assuntos = Assunto.objects.all()
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
            questao = Questao.objects.create(pergunta=pergunta,
                                             curso=nome_curso,
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
            questao.save()

            messages.success(request, "questão editada com Sucesso")
            return redirect('home')
        return render(request, 'pagina_principal/editar_questao.html',
                      {'questao': questao, 'assuntos': assuntos})
    else:
        mensagem = ('Apenas o autor dessa questão pode altera-la')
        messages.error(request, mensagem)
        return redirect('home')
