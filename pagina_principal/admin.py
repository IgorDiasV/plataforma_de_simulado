from django.contrib import admin
from .models import Questao, Assunto, Simulado
from django.contrib import admin
# from usuarios.models import Usuario

# @admin.register(Usuario)
# class UserAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Questao)
admin.site.register(Assunto)
admin.site.register(Simulado)
