# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Atividade(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)
    # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')
    # Field name made lowercase.
    capacidademaxima = models.IntegerField(db_column='CapacidadeMaxima')
    # Field name made lowercase.
    duracao = models.IntegerField(db_column='Duracao')
    # Field name made lowercase.
    publicoalvo = models.CharField(db_column='Publicoalvo', max_length=255)
    # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey(
        'coordenadores.Coordenador', models.CASCADE, db_column='CoordenadorUtilizadorID')
    professoruniversitarioutilizadorid = models.ForeignKey(
        'utilizadores.Professoruniversitario', models.CASCADE, db_column='ProfessorUniversitarioUtilizadorID')  # Field name made lowercase.
    # Field name made lowercase.
    nrcolaboradoresnecessario = models.IntegerField(
        db_column='nrColaboradoresNecessario')
    # Field name made lowercase.
    datasubmissao = models.DateField(
        db_column='dataSubmissao', blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Atividade'


class Atividadesessao(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    atividadeid = models.ForeignKey(
        Atividade, models.CASCADE, db_column='AtividadeID')
    # Field name made lowercase.
    sessaoid = models.ForeignKey(
        'Sessao', models.CASCADE, db_column='SessaoID')

    class Meta:
        db_table = 'AtividadeSessao'


class Sessao(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    espacoid = models.ForeignKey(
        'Espaco', models.CASCADE, db_column='EspacoID')
    # Field name made lowercase.
    horarioid = models.ForeignKey(
        'configuracao.Horario', models.CASCADE, db_column='HorarioID')
    # Field name made lowercase.
    ninscritos = models.IntegerField(db_column='NInscritos')
    # Field name made lowercase.
    vagas = models.IntegerField(db_column='Vagas')

    class Meta:
        db_table = 'Sessao'


class Espaco(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    edificio = models.CharField(
        db_column='Edificio', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    andar = models.CharField(
        db_column='Andar', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)

    class Meta:
        db_table = 'Espaco'


class Materiais(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    atividadeid = models.ForeignKey(
        Atividade, models.CASCADE, db_column='AtividadeID')
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Materiais'


class Unidadeorganica(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=255)
    # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)
    # Field name made lowercase.
    campusid = models.ForeignKey(
        'configuracao.Campus', models.CASCADE, db_column='CampusID')

    class Meta:
        db_table = 'UnidadeOrganica'


class Anfiteatro(models.Model):
    # Field name made lowercase.
    espacoid = models.OneToOneField(
        Espaco, models.CASCADE, db_column='EspacoID', primary_key=True)
    # Field name made lowercase.
    espacoedificio = models.CharField(
        db_column='EspacoEdificio', max_length=255)

    class Meta:
        db_table = 'Anfiteatro'


class Arlivre(models.Model):
    # Field name made lowercase.
    espacoid = models.OneToOneField(
        Espaco, models.CASCADE, db_column='EspacoID', primary_key=True)
    # Field name made lowercase.
    espacoedificio = models.CharField(
        db_column='EspacoEdificio', max_length=255)

    class Meta:
        db_table = 'ArLivre'
