# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from utilizadores.models import *
from configuracao.models import *
from inscricoes.models import *
from notificacoes.models import *
from atividades.models import *

class Coordenador(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=True, null=True)  # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='unidadeOrganicaID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Coordenador'


class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    concluida = models.IntegerField(db_column='Concluida')  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)  # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey(Coordenador, models.DO_NOTHING, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    colaboradorutilizadorid = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='ColaboradorUtilizadorID')  # Field name made lowercase.
    sessaoid = models.ForeignKey('Sessao', models.DO_NOTHING, db_column='SessaoID')  # Field name made lowercase.
    inscricaoid = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricaoid', blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=64)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tarefa'
        