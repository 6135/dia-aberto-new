from django.contrib import admin

from .models import Tarefa,TarefaAcompanhar, TarefaAuxiliar,TarefaOutra
# Register your models here.
admin.site.register(Tarefa)

admin.site.register(TarefaAcompanhar)

admin.site.register(TarefaAuxiliar)

admin.site.register(TarefaOutra)