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
