from django.urls import path, include

from . import views

app_name = 'colaboradores'


urlpatterns = [
    path('consultartarefas', views.consultar_tarefas.as_view(), name='consultar-tarefas'),
    path('consultartarefasold', views.consultar_tarefas_old, name='consultar-tarefas-old'),
    path('concluirtarefa/<int:id>', views.concluir_tarefa, name='concluir-tarefa'),
    path('iniciartarefa/<int:id>', views.iniciar_tarefa, name='iniciar-tarefa'),
    path('cancelartarefa/<int:id>', views.cancelar_tarefa, name='cancelar-tarefa'),
    path('rejeitarcancelamentotarefa/<int:id_notificacao>',
         views.rejeitar_cancelamento_tarefa, name='rejeitar-cancelamento-tarefa'),
    path('validarcancelamentotarefa/<int:id_notificacao>',
         views.validar_cancelamento_tarefa, name='validar-cancelamento-tarefa'),
]
