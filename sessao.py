# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Sessao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey('Horario', models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    ninscritos = models.IntegerField(db_column='NInscritos')  # Field name made lowercase.
    vagas = models.IntegerField(db_column='Vagas')  # Field name made lowercase.
    atividadeid = models.ForeignKey('Atividade', models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.
    dia = models.DateField(db_column='Dia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sessao'
