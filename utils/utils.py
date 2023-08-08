from simulados.models import Simulado, RespostaQuestaoSimulado
from pagina_principal.models import Questao, Assunto


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


def lista_questoes(usuario=None, filtro_assunto=[], anos=[]):
    questoes = Questao.objects.all()
    assuntos = Assunto.objects.all()
    anos_questoes = [questao.ano for questao in questoes]
    anos_questoes = list(set(anos_questoes))
    if len(filtro_assunto) > 0:
        questoes = questoes.filter(assuntos__id__in=filtro_assunto)
    if usuario is not None:
        questoes = questoes.filter(autor=usuario)
    if len(anos) > 0:
        questoes = questoes.filter(ano__in=anos)
    return questoes, assuntos, anos_questoes


def formatar_tempo(segundos):
    horas = int((segundos/3600))
    segundos -= horas*3600
    minutos = int(segundos/60)
    segundos -= minutos * 60
    tempo_formatado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    return tempo_formatado
