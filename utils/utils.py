from simulados.models import Simulado, RespostaQuestaoSimulado


def qtd_perguntas(id_simulado):
    simulado = Simulado.objects.filter(id=id_simulado).first()
    return len(simulado.questoes.all())


def qtd_acertos(id_resposta):
    respostas_questoes = RespostaQuestaoSimulado.objects.filter(resposta_simulado__id=id_resposta)  # noqa: E501
    acertos = 0
    for resposta_questao in respostas_questoes:
        if resposta_questao.resposta == resposta_questao.questao.alternativa_correta:  # noqa: E501
            acertos += 1
    return acertos


def valores_que_sairam_da_lista(lista_antiga: list, lista_nova: list) -> list:
    valores_sairam = []

    for valor in lista_antiga:
        if valor not in lista_nova:
            valores_sairam.append(valor)
    return valores_sairam


def assuntos_removidos(assuntos_atingos: list, assuntos_novos: list) -> list:
    return valores_que_sairam_da_lista(assuntos_atingos, assuntos_novos)


def assuntos_adicionados(assuntos_atingos: list, assuntos_novos: list) -> list:

    return valores_que_sairam_da_lista(assuntos_novos, assuntos_atingos)
