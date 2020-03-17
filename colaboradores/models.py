# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    concluida = models.IntegerField(db_column='Concluida')  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)  # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey('coordenadores.Coordenador', models.DO_NOTHING, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    colaboradorutilizadorid = models.ForeignKey('Colaborador', models.DO_NOTHING, db_column='ColaboradorUtilizadorID')  # Field name made lowercase.
    atividadeid = models.ForeignKey('atividades.Atividade', models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tarefa'


class Colaborador(models.Model):
    utilizadorid = models.OneToOneField('utilizadoes.Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    curso = models.CharField(db_column='Curso', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Colaborador'


class Colaboradorhorario(models.Model):
    colaboradorutilizadorid = models.OneToOneField(Colaborador, models.DO_NOTHING, db_column='ColaboradorUtilizadorID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey('configuracao.Horario', models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    horarioinicio = models.DateField(db_column='HorarioInicio')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ColaboradorHorario'
        unique_together = (('colaboradorutilizadorid', 'horarioid', 'horarioinicio'),)
