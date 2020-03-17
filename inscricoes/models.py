# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Inscricao(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nrinscricao = models.IntegerField(db_column='NrInscricao')
    ano = models.IntegerField(db_column='Ano')  # Field name made lowercase.
    # Field name made lowercase.
    local = models.CharField(db_column='Local', max_length=128)
    # Field name made lowercase.
    areacientifica = models.CharField(
        db_column='AreaCientifica', max_length=64)
    # Field name made lowercase.
    participanteutilizadorid = models.ForeignKey(
        'utilizadores.Participante', models.CASCADE, db_column='ParticipanteUtilizadorID')
    # Field name made lowercase.
    diaabertoid = models.ForeignKey(
        'configuracao.Diaaberto', models.CASCADE, db_column='DiaAbertoID')

    class Meta:
        db_table = 'Inscricao'


class Inscricaocoletiva(models.Model):
    # Field name made lowercase.
    inscricaoid = models.OneToOneField(
        Inscricao, models.CASCADE, db_column='InscricaoID', primary_key=True)
    # Field name made lowercase.
    escolaid = models.ForeignKey(
        'Escola', models.CASCADE, db_column='EscolaID')
    # Field name made lowercase.
    nralunos = models.IntegerField(db_column='nrAlunos')
    # Field name made lowercase.
    nresponsaveis = models.IntegerField(db_column='nResponsaveis')
    turma = models.CharField(max_length=255)

    class Meta:
        db_table = 'InscricaoColetiva'
        unique_together = (('inscricaoid', 'escolaid'),)


class Inscricaoindividual(models.Model):
    # Field name made lowercase.
    inscricaoid = models.OneToOneField(
        Inscricao, models.CASCADE, db_column='InscricaoID', primary_key=True)
    # Field name made lowercase.
    nracompanhantes = models.IntegerField(
        db_column='nrAcompanhantes', blank=True, null=True)

    class Meta:
        db_table = 'InscricaoIndividual'


class Inscricaoprato(models.Model):
    # Field name made lowercase.
    inscricaoid = models.OneToOneField(
        Inscricao, models.CASCADE, db_column='InscricaoID', primary_key=True)
    # Field name made lowercase.
    pratoid = models.ForeignKey(
        'configuracao.Prato', models.CASCADE, db_column='PratoID')
    # Field name made lowercase.
    nrpessoas = models.IntegerField(db_column='NrPessoas')

    class Meta:
        db_table = 'InscricaoPrato'
        unique_together = (('inscricaoid', 'pratoid'),)


class Inscricaosessao(models.Model):
    # Field name made lowercase.
    inscricaoid = models.OneToOneField(
        Inscricao, models.CASCADE, db_column='InscricaoID', primary_key=True)
    # Field name made lowercase.
    sessaoid = models.ForeignKey(
        'atividades.Sessao', models.CASCADE, db_column='SessaoID')
    # Field name made lowercase.
    nrparticipantes = models.IntegerField(db_column='nrParticipantes')

    class Meta:
        db_table = 'InscricaoSessao'
        unique_together = (('inscricaoid', 'sessaoid'),)


class Inscricaotransporte(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    inscricaoid = models.ForeignKey(
        Inscricao, models.CASCADE, db_column='InscricaoID')
    # Field name made lowercase.
    transporteid = models.ForeignKey(
        'configuracao.Transporte', models.CASCADE, db_column='TransporteID')
    # Field name made lowercase.
    nrparticipantes = models.IntegerField(db_column='NrParticipantes')

    class Meta:
        db_table = 'InscricaoTransporte'


class Escola(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)
    # Field name made lowercase.
    local = models.CharField(db_column='Local', max_length=255)
    # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=16)
    # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)

    class Meta:
        db_table = 'Escola'
