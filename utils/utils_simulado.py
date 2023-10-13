from datetime import datetime


def obter_valor_ou_zero(request, campos):
    valores = []
    for campo in campos:
        valor = request.POST.get(campo)
        if valor is None or valor == "":
            valores.append(0)
        else:
            valores.append(int(valor))
    return valores


def calcular_tempo_prova(request):
    horas = int(request.POST.get("horas", 0))
    minutos = int(request.POST.get("minutos", 0))
    segundos = int(request.POST.get("segundos", 0))
    return horas * 3600 + minutos * 60 + segundos


def  calcular_data(request):
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

    return data_hora_inicial, data_hora_final