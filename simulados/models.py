from django.db import models
from usuarios.models import Usuario
from questoes.models import Questao
import uuid


class Simulado(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=300)
    questoes = models.ManyToManyField(Questao)
    autor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=True
    )
    compartilhado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo


class SimuladoCompartilhado(models.Model):
    id = models.AutoField(primary_key=True)
    simulado = models.OneToOneField(Simulado, on_delete=models.CASCADE)
    link = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tempo_de_prova = models.IntegerField(default=0)
    qtd_tentativas = models.IntegerField(default=0)
    data_inicio = models.DateTimeField(default=None, null=True, blank=True)
    data_fim = models.DateTimeField(default=None, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"compartilhado o simulado ({self.simulado.titulo})"


class RespostaSimulado(models.Model):
    id = models.AutoField(primary_key=True)
    simulado_respondido = models.ForeignKey(SimuladoCompartilhado,
                                            on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"reposta {self.id} do simulado {self.simulado_respondido.id}"


class RespostaQuestaoSimulado(models.Model):
    id = models.AutoField(primary_key=True)
    resposta_simulado = models.ForeignKey(RespostaSimulado,
                                          on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao,
                                on_delete=models.CASCADE)
    resposta = models.CharField(null=False, max_length=1)

    def __str__(self) -> str:
        return f"Respota {self.id} da questão {self.questao.id}"
