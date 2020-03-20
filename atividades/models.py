# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from utilizadores.models import *
from coordenadores.models import *
from configuracao.models import *
from inscricoes.models import *
from notificacoes.models import *


class Anfiteatro(models.Model):
    espacoid = models.OneToOneField('Espaco', models.DO_NOTHING, db_column='EspacoID', primary_key=True)  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'Anfiteatro'


class Arlivre(models.Model):
    espacoid = models.OneToOneField('Espaco', models.DO_NOTHING, db_column='EspacoID', primary_key=True)  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'ArLivre'


class Atividade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase.
    unidadeorganica = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='UnidadeOrganica')  # Field name made lowercase.
    publicoalvo = models.CharField(db_column='Publicoalvo', max_length=255)  # Field name made lowercase.
    nrcolaboradoresnecessario = models.IntegerField(db_column='nrColaboradoresNecessario')  # Field name made lowercase.
    tipos = (("laboral", "Atividade Laboral"),("tertulia", "Tertulia"),("palestra", "Palestra"))
    tipo = models.CharField(db_column='Tipo', max_length=128, choices=tipos )  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=64, blank=True, null=True)  # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey('coordenadores.Coordenador', models.DO_NOTHING, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    professoruniversitarioutilizadorid = models.ForeignKey('utilizadores.Professoruniversitario', models.DO_NOTHING, db_column='ProfessorUniversitarioUtilizadorID')  # Field name made lowercase.
    datasubmissao = models.DateTimeField(db_column='dataSubmissao',auto_now_add=True)  # Field name made lowercase.
    dataalteracao = models.DateTimeField(db_column='dataAlteracao',auto_now=True)  # Field name made lowercase.
 
    class Meta:
        db_table = 'Atividade'


class Atividadesessao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    atividadeid = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.
    sessaoid = models.ForeignKey('Sessao', models.DO_NOTHING, db_column='SessaoID')  # Field name made lowercase.

    class Meta:
        db_table = 'AtividadeSessao'

class Espaco(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    edificio = models.CharField(db_column='Edificio', max_length=255, blank=True, null=True)  # Field name made lowercase.
    andar = models.CharField(db_column='Andar', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'Espaco'

class Materiais(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    atividadeid = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Materiais'

class Sessao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    espacoid = models.ForeignKey(Espaco, models.DO_NOTHING, db_column='EspacoID')  # Field name made lowercase.
    horarioid = models.ForeignKey(Horario, models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    ninscritos = models.IntegerField(db_column='NInscritos')  # Field name made lowercase.
    vagas = models.IntegerField(db_column='Vagas')  # Field name made lowercase.
    duracaomedia = models.IntegerField(db_column='duracaoMedia', blank=True, null=True)  # Field name made lowercase.
    participantesmaximo = models.IntegerField(db_column='participantesMaximo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Sessao'

class Unidadeorganica(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=255)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.

    class Meta:
        db_table = 'UnidadeOrganica'

