# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Atividade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase.
    publicoalvo = models.CharField(db_column='Publicoalvo', max_length=255)  # Field name made lowercase.
    nrcolaboradoresnecessario = models.IntegerField(db_column='nrColaboradoresNecessario')  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=128)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=64, blank=True, null=True)  # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey('Coordenador', models.DO_NOTHING, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    professoruniversitarioutilizadorid = models.ForeignKey('Professoruniversitario', models.DO_NOTHING, db_column='ProfessorUniversitarioUtilizadorID')  # Field name made lowercase.
    datasubmissao = models.DateTimeField(db_column='dataSubmissao')  # Field name made lowercase.
    dataalteracao = models.DateTimeField(db_column='dataAlteracao')  # Field name made lowercase.
    diaabertoid = models.ForeignKey('Diaaberto', models.DO_NOTHING, db_column='diaAbertoID')  # Field name made lowercase.
    duracaoesperada = models.IntegerField(db_column='duracaoEsperada', blank=True, null=True)  # Field name made lowercase.
    participantesmaximo = models.IntegerField(db_column='participantesMaximo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Atividade'
