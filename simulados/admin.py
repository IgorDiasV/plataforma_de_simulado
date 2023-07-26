from django.contrib import admin
from .models import Simulado, SimuladoCompartilhado, RespostaSimulado
from .models import RespostaQuestaoSimulado


class SimuladoCompartilhadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'simulado', 'link')


admin.site.register(Simulado)
admin.site.register(SimuladoCompartilhado, SimuladoCompartilhadoAdmin)
admin.site.register(RespostaSimulado)
admin.site.register(RespostaQuestaoSimulado)
