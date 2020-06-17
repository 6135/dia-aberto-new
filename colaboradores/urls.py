from django.urls import path, include

from . import views

app_name = 'colaboradores'


urlpatterns = [

    path('consultartarefas', views.consultar_tarefas, name='consultar-tarefas'),
    path('concluirtarefa/<int:id>', views.concluir_tarefa, name='concluir-tarefa'),
    path('iniciartarefa/<int:id>', views.iniciar_tarefa, name='iniciar-tarefa'),
    path('cancelartarefa/<int:id>', views.cancelar_tarefa, name='cancelar-tarefa'),
    path('rejeitarcancelamentotarefa/<int:id>',
         views.rejeitar_cancelamento_tarefa, name='rejeitar-cancelamento-tarefa'),
    path('validarcancelamentotarefa/<int:id>',
         views.validar_cancelamento_tarefa, name='validar-cancelamento-tarefa'),
]
