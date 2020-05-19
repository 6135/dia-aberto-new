
from django.db import models

from atividades.models import *
from inscricoes.models import *


class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    estado = models.CharField(max_length=64)
    coord = models.ForeignKey('utilizadores.Coordenador', models.CASCADE, db_column='CoordenadorUtilizadorID',null=True)  # Field name made lowercase.
    colab = models.ForeignKey('utilizadores.Colaborador', models.CASCADE, db_column='ColaboradorUtilizadorID',null=True,blank=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Tarefa'




class TarefaAcompanhar(Tarefa):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    inscricaoid = models.ForeignKey(Inscricao, models.CASCADE, db_column='inscricaoid')
    origem = models.CharField(max_length=255, db_column='origem', blank=False, null=False)
    destino = models.CharField(max_length=255, db_column='destino', blank=False, null=False)
    horario = models.TimeField(blank=False, null=False)
    dia = models.DateField()
    
    class Meta:
        db_table = 'TarefaAcompanhar'


class TarefaAuxiliar(Tarefa):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    sessaoid = models.ForeignKey('atividades.Sessao', models.CASCADE, db_column='sessaoid')

    class Meta:
        db_table = 'TarefaAuxiliar'


class TarefaOutra(Tarefa):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    descricao = models.TextField(db_column='descricao', blank=False, null=False)
    horario = models.TimeField(blank=False, null=False)
    dia = models.DateField()

    class Meta:
        db_table = 'TarefaOutra'