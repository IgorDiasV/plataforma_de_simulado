from django.db import models
from usuarios.models import Usuario


class Assunto(models.Model):
    id = models.AutoField(primary_key=True)
    nome_assunto = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nome_assunto


class Questao(models.Model):

    id = models.AutoField(primary_key=True)
    assuntos = models.ManyToManyField(Assunto)
    curso = models.TextField(null=False, default="Não Cadastrado")
    pergunta = models.TextField(default='none')    
    alternativa_a = models.TextField(null=False, default='none')
    alternativa_b = models.TextField(null=False, default='none')
    alternativa_c = models.TextField(null=False, default='none')
    alternativa_d = models.TextField(null=False, default='none')
    alternativa_e = models.TextField(null=False, default='none')
    alternativa_correta = models.CharField(max_length=1,
                                           null=False, default='0')
    autor = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return str(self.id)
