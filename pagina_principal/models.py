from django.db import models


class Assunto(models.Model):
    id = models.AutoField(primary_key = True)
    nome_assunto = models.CharField(max_length = 150 , unique =True )

    def __str__(self):
        return self.nome_assunto

class Questao(models.Model):

    id = models.AutoField(primary_key = True)
    assuntos = models.ManyToManyField(Assunto)
    n_questao = models.IntegerField(null = False, default=0)
    tipo_questao = models.CharField(max_length=120, null = False, default='none')
    curso = models.TextField(null = False, default = "Não Cadastrado")
    pergunta = models.TextField(default='none')    
    alternativa_a = models.TextField(null = False, default='none')
    alternativa_b = models.TextField(null = False, default='none')
    alternativa_c = models.TextField(null = False, default='none')
    alternativa_d = models.TextField(null = False, default='none')
    alternativa_e = models.TextField(null = False, default='none')
    alternativa_correta = models.CharField(max_length = 1, null = False, default='0')
    
    def __str__(self):
        return str(self.id)
    
class Simulado(models.Model):
    id = models.AutoField(primary_key = True)
    titulo = models.CharField(max_length=300)
    questoes = models.ManyToManyField(Questao)

    def __str__(self):
        return self.titulo
