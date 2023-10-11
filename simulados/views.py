from django.shortcuts import render, redirect, get_object_or_404
from questoes.models import Questao, Assunto
from .models import Simulado, SimuladoCompartilhado
from .models import RespostaSimulado, RespostaQuestaoSimulado
from random import sample
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.contrib import messages
from django.http.response import Http404
from django.urls import reverse
from utils.utils import qtd_perguntas, qtd_acertos, formatar_tempo_str, formatar_tempo_int     # noqa: E501
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.utils import lista_questoes, get_parametros_url, get_grafico
from utils.utils_simulado import calcular_tempo_prova


def simulado(request):
    simulado_id = request.POST["simulado_id"]
    simulado = get_object_or_404(Simulado, id=simulado_id)
    questoes = simulado.questoes.all()

    return render(
        request,
        "simulados/simulado.html",
        {"questoes": questoes, "simulado": simulado, "tempo_de_prova": ""},
    )


def gerar_link(request):
    if request.method == "POST":
        qtd_tentativas = int(request.POST.get("qtd_tentativas", 0))
        tempo_de_prova = calcular_tempo_prova(request)

        id_simulado = request.POST["id_simulado"]
        data_hora_inicial = None
        data_hora_final = None
        if request.POST.get("data_limite"):
            formato = "%Y-%m-%d %H:%M"

            try:
                data_inicial = request.POST["data_inicial"]
                hora_inicial = request.POST["horario_inicial"]

                data_hora_inicial_str = f"{data_inicial} {hora_inicial}"
                data_hora_inicial = datetime.strptime(
                                        data_hora_inicial_str, formato)

                data_final = request.POST["data_final"]
                hora_final = request.POST["horario_final"]

                data_hora_final_str = f"{data_final} {hora_final}"
                data_hora_final = datetime.strptime(
                                    data_hora_final_str, formato)
            except ValueError:
                data_hora_inicial = None
                data_hora_final = None

        simulado = Simulado.objects.filter(id=id_simulado).first()
        if request.POST['tipo'] == 'criar':
            SimuladoCompartilhado.objects.create(
                simulado=simulado,
                tempo_de_prova=tempo_de_prova,
                qtd_tentativas=qtd_tentativas,
                data_inicio=data_hora_inicial,
                data_fim=data_hora_final,
            )
        else:
            link = request.POST['link_parcial']
            simulado_compartilhado = SimuladoCompartilhado.objects.filter(
                                        link=link).first()
            simulado_compartilhado.tempo_de_prova = tempo_de_prova
            simulado_compartilhado.qtd_tentativas = qtd_tentativas
            simulado_compartilhado.data_inicio = data_inicial
            simulado_compartilhado.data_fim = data_final
            simulado_compartilhado.save()

        return redirect("simulados:lista_simulados")
    else:
        return Http404()


@login_required(login_url="usuarios:login", redirect_field_name="next")
def dados_simulado(request, simulado_link):
    respostas_simulado = RespostaSimulado.objects.filter(
        simulado_respondido__link=simulado_link
    )
    usuario = Usuario.objects.filter(user=request.user).first()
    qtd_respostas = len(respostas_simulado.filter(usuario=usuario))
    simulado_compartilhado = get_object_or_404(
        SimuladoCompartilhado, link=simulado_link
    )
    tempo_de_prova = simulado_compartilhado.tempo_de_prova
    tempo_formatado = "Sem Tempo limite"
    disponivel_responder_simulado = True
    if tempo_de_prova > 0:
        tempo_formatado = formatar_tempo_str(tempo_de_prova)

    qtd_tentativas = simulado_compartilhado.qtd_tentativas

    if qtd_tentativas == 0:
        qtd_tentativas = "Sem limite de tentativas"
    else:
        qtd_tentativas -= qtd_respostas

        if qtd_tentativas == 0:
            disponivel_responder_simulado = False

    disponibilidade = "O simulado não possue data limite"
    if (simulado_compartilhado.data_inicio is not None) and (
        simulado_compartilhado.data_fim is not None
    ):
        formato_br = "%d/%m/%Y %H:%M"
        data_inicio = simulado_compartilhado.data_inicio.replace(tzinfo=None)
        data_inicio_str = data_inicio.strftime(formato_br)
        data_fim = simulado_compartilhado.data_fim.replace(tzinfo=None)
        data_fim_str = data_fim.strftime(formato_br)
        disponibilidade = f"{data_inicio_str} até {data_fim_str}"

        data_atual = datetime.now()
        if not (data_atual > data_inicio and data_atual < data_fim):
            disponibilidade = "O simulado não está mais disponivel"
            disponivel_responder_simulado = False

    simulado = simulado_compartilhado.simulado
    titulo = simulado.titulo
    qtd_questoes = len(simulado.questoes.all())
    professor = simulado.autor.user
    nome_professor = professor.first_name + " " + professor.last_name

    return render(
        request,
        "simulados/dados_simulado.html",
        {
            "titulo": titulo,
            "professor": nome_professor,
            "qtd_questoes": qtd_questoes,
            "link": simulado_link,
            "tempo_de_prova": tempo_formatado,
            "qtd_tentativas": qtd_tentativas,
            "disponibilidade": disponibilidade,
            "disponivel_responder_simulado": disponivel_responder_simulado,
        },
    )


@login_required(login_url="usuarios:login", redirect_field_name="next")
def responder_simulado(request):
    if request.method == "POST":
        link = request.POST["link"]
        if not request.session.get("inicio_simulado", None):
            request.session["inicio_simulado"] = datetime.now().ctime()
        inicio_simulado = request.session.get("inicio_simulado", None)

        simulado_compartilhado = get_object_or_404(
                                    SimuladoCompartilhado, link=link)

        tempo_de_prova = simulado_compartilhado.tempo_de_prova
        simulado = simulado_compartilhado.simulado
        questoes = simulado.questoes.all()

        return render(
            request,
            "simulados/simulado.html",
            {
                "questoes": questoes,
                "simulado": simulado,
                "link": link,
                "inicio_simulado": inicio_simulado,
                "tempo_de_prova": tempo_de_prova,
            },
        )
    else:
        return Http404()


@login_required(login_url="usuarios:login", redirect_field_name="next")
def salvar_resposta(request):
    link = ""
    dados_questoes = []
    for name, value in request.POST.items():
        if name == "link":
            link = value
        elif name != "csrfmiddlewaretoken":
            aux = {}
            aux["id_questao"] = name
            aux["resposta"] = value
            dados_questoes.append(aux)

    simulado_compartilhado = get_object_or_404(
                                SimuladoCompartilhado, link=link)

    usuario = Usuario.objects.filter(user=request.user).first()
    resposta_simulado = RespostaSimulado.objects.create(
        simulado_respondido=simulado_compartilhado, usuario=usuario
    )
    for dado_questao in dados_questoes:
        id_questao = int(dado_questao["id_questao"])
        questao = get_object_or_404(Questao, id=id_questao)
        resposta = dado_questao["resposta"]
        RespostaQuestaoSimulado.objects.create(
            resposta_simulado=resposta_simulado,
            questao=questao,
            resposta=resposta,
        )
    messages.success(request, "Respotas Salva")
    del request.session["inicio_simulado"]
    return redirect("home")


@login_required(login_url="usuarios:login", redirect_field_name="next")
def respostas_do_simulado(request):
    if request.method == "POST":
        id_simulado = request.POST["id_simulado"]
        respostas = RespostaSimulado.objects.filter(
            simulado_respondido__simulado__id=id_simulado
        )
        respostas_por_questao = RespostaQuestaoSimulado.objects.filter(
            resposta_simulado__in=respostas
        )
        img_grafico = get_grafico(respostas_por_questao)
        qtd_perguntas_simulado = qtd_perguntas(id_simulado)
        alunos_que_responderam = []
        for resposta in respostas:
            qtd_acertos_aluno = qtd_acertos(resposta.id)
            desempenho = f"{qtd_acertos_aluno}/{qtd_perguntas_simulado}"
            nome = (
                f"{resposta.usuario.user.first_name} {resposta.usuario.user.last_name}"  # noqa: E501
            )
            email = resposta.usuario.user.email
            alunos_que_responderam.append(
                {
                    "id_resposta": resposta.id,
                    "nome": nome,
                    "email": email,
                    "desempenho": desempenho,
                }
            )

        return render(
            request,
            "simulados/respostas_do_simulado.html",
            {
             "alunos": alunos_que_responderam,
             "grafico": img_grafico
             },
        )
    else:
        return Http404()


@login_required(login_url="usuarios:login", redirect_field_name="next")
def resposta_aluno(request):
    if request.method == "POST":
        id = request.POST["id_resposta"]
        respostas_questoes = RespostaQuestaoSimulado.objects.filter(
            resposta_simulado__id=id
        )
        img_grafico = get_grafico(respostas_questoes)
        simulado_respondido = RespostaSimulado.objects.filter(id=id)
        simulado_respondido = simulado_respondido.first().simulado_respondido
        questoes_simulados = simulado_respondido.simulado.questoes.all()

        dados_questao = []
        for questao in questoes_simulados:
            resposta_questao = respostas_questoes.filter(questao=questao)
            classe = ""
            key = ""
            if len(resposta_questao) > 0:
                resposta_questao = resposta_questao.first()
                classe = "wrong_answer"
                if (
                    resposta_questao.resposta
                    == resposta_questao.questao.alternativa_correta
                ):
                    classe = "right_answer"
                key = f"classe_alternativa_{resposta_questao.resposta.lower()}"
            dados_questao.append({"questao": questao, key: classe})

        return render(
            request,
            "simulados/exibir_resultado.html",
            {
             "dados_questoes": dados_questao,
             "grafico": img_grafico
             },
        )
    else:
        return Http404()


@login_required(login_url="usuarios:login", redirect_field_name="next")
def lista_simulados(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    simulados = Simulado.objects.filter(autor=usuario).order_by("-id")
    respostas = RespostaQuestaoSimulado.objects.all()
    respostas = respostas.filter(resposta_simulado__simulado_respondido__simulado__autor=usuario)  # noqa: E501
    img_grafico = get_grafico(respostas)
    simulados_e_link = []

    n_pagina = request.GET.get('page', '1')
    simulados_paginacao = Paginator(simulados, 5)
    try:
        simulados = simulados_paginacao.page(n_pagina)
    except (EmptyPage, PageNotAnInteger):
        simulados = simulados_paginacao.page(1)

    for simulado in simulados:
        simulado_compartilhado = SimuladoCompartilhado.objects.filter(
            simulado=simulado
        ).first()
        aux = {}
        aux["simulado"] = simulado

        if simulado_compartilhado is not None:
            link = simulado_compartilhado.link
            aux["link_parcial"] = link
            url_completa = (
                f"{request.scheme}://"
                f"{request.get_host()}"
                f"{reverse('simulados:dados_simulado', args=[link])}"
            )
            aux["link"] = url_completa
            data_inicio = simulado_compartilhado.data_inicio
            data_fim = simulado_compartilhado.data_fim

            data_inicio_str = ""
            data_fim_str = ""
            hora_inicio_str = ""
            hora_fim_str = ""

            if data_inicio is not None:
                formato_data = "%Y-%m-%d"
                formato_hora = "%H:%M"

                data_inicio = data_inicio.replace(tzinfo=None)
                data_fim = data_fim.replace(tzinfo=None)

                data_inicio_str = data_inicio.strftime(formato_data)
                data_fim_str = data_fim.strftime(formato_data)

                hora_inicio_str = data_inicio.strftime(formato_hora)
                hora_fim_str = data_fim.strftime(formato_hora)

            aux['data_inicio'] = data_inicio_str
            aux['data_fim'] = data_fim_str
            aux['hora_inicio'] = hora_inicio_str
            aux['hora_fim'] = hora_fim_str

            tempo_de_prova = simulado_compartilhado.tempo_de_prova

            horas = ""
            minutos = ""
            segundos = ""

            if tempo_de_prova != 0:
                horas, minutos, segundos = formatar_tempo_int(tempo_de_prova)

            aux['tempo_horas'] = horas
            aux['tempo_minutos'] = minutos
            aux['tempo_segundos'] = segundos

            qtd_tentativas = simulado_compartilhado.qtd_tentativas

            if qtd_tentativas == 0:
                qtd_tentativas = ''

            aux['qtd_tentativas'] = qtd_tentativas
        simulados_e_link.append(aux)
    return render(
        request, "simulados/lista_simulados.html",
        {"simulados_e_links": simulados_e_link,
         "grafico": img_grafico,
         "simulados_paginacao": simulados
         }
    )


@login_required(login_url="usuarios:login", redirect_field_name="next")
def criar_simulado(request):
    # TODO Verificar se todos os campos foram preenchidos para evitar erros
    # TODO verificar se a quantiade de questões disponiveis é suficiente
    # para criar o simulado ex: foi pedido para criar um simulado
    # com 10 questões, mas só tem 5 questões cadastradas

    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        assuntos = Assunto.objects.all()
        if request.method == "POST":
            questoes = Questao.objects.all()

            titulo = request.POST["titulo"]
            assuntos_ids = request.POST.getlist("assuntos")
            qtd_questoes = int(request.POST["qtd_questoes"])

            if len(assuntos_ids) != 0:
                questoes = questoes.filter(
                                assuntos__id__in=assuntos_ids).distinct()

            indices_para_sorteio = list(range(0, len(questoes)))
            indices_escolhidos = sample(indices_para_sorteio, qtd_questoes)
            simulado = Simulado.objects.create(titulo=titulo, autor=usuario)
            for indice in indices_escolhidos:
                simulado.questoes.add(questoes[indice])
            return redirect("simulados:lista_simulados")
        return render(request, "simulados/criar_simulado.html",
                      {"assuntos": assuntos})
    else:
        mensagem = "Seu perfil é de aluno, Apenas professores podem criar simulados"  # noqa: E501
        messages.error(request, mensagem)
        return redirect("home")


@login_required(login_url="usuarios:login", redirect_field_name="next")
def criar_simulado_manualmente(request, tipo):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        if request.method == "POST":
            id_questoes_escolhidas = []
            questoes_escolhidas = None
            assuntos_ids = []
            id = ""
            titulo = ""
            if tipo == 'editar':
                id = request.POST['id_simulado']
                simulado = Simulado.objects.filter(id=id).first()
                titulo = simulado.titulo
                questoes_escolhidas = simulado.questoes.all()
                id_questoes_escolhidas = [questao.id for questao in questoes_escolhidas]  # noqa: E501

            dados_questoes = lista_questoes()
            questoes = dados_questoes['questoes']
            assuntos = dados_questoes['assuntos']
            anos = dados_questoes['anos_questoes']
            origem = dados_questoes['origem']

            page = ""
            questoes_paginacao = Paginator(questoes, 5)

            page = questoes_paginacao.page(1)

            return render(
                request,
                "simulados/criar_simulado_manualmente.html",
                {
                    "tipo": tipo,
                    "id_simulado": id,
                    "questoes": page,
                    "assuntos": assuntos,
                    "id_questoes_escolhidas": id_questoes_escolhidas,
                    "questoes_escolhidas": questoes_escolhidas,
                    "titulo": titulo,
                    "id_filtro_assunto": assuntos_ids,
                    "anos_questoes": anos,
                    "origem": origem
                },
            )

        lista_parametros = ['id_assuntos_filtro',
                            'id_anos_filtro',
                            'ids_filtro_origens',
                            'id_questao']
        valores_parametros = get_parametros_url(request, lista_parametros)

        assuntos_ids = valores_parametros['id_assuntos_filtro']
        anos_ids = valores_parametros['id_anos_filtro']
        origens = valores_parametros['ids_filtro_origens']
        id_questoes_escolhidas = valores_parametros['id_questao']

        n_pagina = request.GET.get("page", "1")
        titulo = request.GET.get("titulo", "")
        id = request.GET.get("id_simulado", "")
        questoes_escolhidas = ""

        if len(id_questoes_escolhidas) > 0:
            questoes_escolhidas = Questao.objects.all().filter(
                id__in=id_questoes_escolhidas
            )

        dados_questoes = lista_questoes(
            filtro_assunto=assuntos_ids,
            anos=anos_ids,
            origem=origens
        )

        questoes = dados_questoes['questoes']
        assuntos = dados_questoes['assuntos']
        anos = dados_questoes['anos_questoes']
        origem = dados_questoes['origem']

        page = ""
        questoes_paginacao = Paginator(questoes, 5)
        try:
            page = questoes_paginacao.page(n_pagina)
        except (EmptyPage, PageNotAnInteger):
            page = questoes_paginacao.page(1)

        return render(
            request,
            "simulados/criar_simulado_manualmente.html",
            {
                "id_simulado": id,
                "tipo": tipo,
                "questoes": page,
                "assuntos": assuntos,
                "id_questoes_escolhidas": id_questoes_escolhidas,
                "questoes_escolhidas": questoes_escolhidas,
                "titulo": titulo,
                "id_filtro_assunto": assuntos_ids,
                "anos_questoes": anos,
                "origem": origem
            },
        )

    else:
        mensagem = "Seu perfil é de aluno, Apenas professores podem criar simulados"  # noqa: E501
        messages.error(request, mensagem)
        return redirect("home")


def save(request, tipo):
    usuario = Usuario.objects.filter(user=request.user).first()
    if usuario.is_teacher:
        if request.method == "POST":
            titulo = request.POST["titulo"]
            id_questoes_escolhidas = request.POST.getlist(
                                        "questoes_escolhidas")
            questoes_escolhidas = Questao.objects.all().filter(
                id__in=id_questoes_escolhidas
            )
            if len(id_questoes_escolhidas) < 1:
                mensagem = 'É precisso selecionar no mínimo uma questão'
                messages.error(request, mensagem)
                return redirect('home')
            if tipo == 'editar':
                id_simulado = request.POST["id_simulado"]
                simulado = Simulado.objects.filter(id=id_simulado).first()
                simulado.titulo = titulo
                simulado.questoes.set(questoes_escolhidas)
                simulado.save()
                messages.success(request, "Simulado Editado com Sucesso")
            else:
                simulado = Simulado.objects.create(titulo=titulo,
                                                   autor=usuario)
                simulado.questoes.set(questoes_escolhidas)
                messages.success(request, "Simulado Criado com Sucesso")

            return redirect("simulados:lista_simulados")
        

def desempenho(request):
    return render(request, 'simulados/desempenho.html')
