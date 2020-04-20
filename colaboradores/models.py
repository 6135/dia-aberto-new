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

class Colaborador(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    curso = models.CharField(db_column='Curso', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Colaborador'


class Colaboradorhorario(models.Model):
    # Field name made lowercase.
    colaboradorutilizadorid = models.OneToOneField(
        Colaborador, models.CASCADE, db_column='ColaboradorUtilizadorID', primary_key=True)
    # Field name made lowercase.
    horarioid = models.ForeignKey(
        'configuracao.Horario', models.CASCADE, db_column='HorarioID')
    # Field name made lowercase.
    horarioinicio = models.DateField(db_column='HorarioInicio')

    class Meta:
        db_table = 'ColaboradorHorario'
        unique_together = (
            ('colaboradorutilizadorid', 'horarioid', 'horarioinicio'),)
