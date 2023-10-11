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