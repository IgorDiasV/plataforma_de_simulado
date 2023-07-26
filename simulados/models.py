from django.db import models
from pagina_principal.models import Questao
from usuarios.models import Usuario


class Simulado(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=300)
    questoes = models.ManyToManyField(Questao)
    autor = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.titulo

