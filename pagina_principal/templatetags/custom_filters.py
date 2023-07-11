from django import template

register = template.Library()
 
@register.filter
def get_id_assunto(questao):
     lista_ids = [str(assunto.id) for assunto in questao.assuntos.all()]
     string_ids = "*".join(lista_ids)
     string_ids = "*"+string_ids+"*"
     return string_ids