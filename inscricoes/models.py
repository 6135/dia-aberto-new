from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField
from configuracao.models import *
from colaboradores.models import *
from utilizadores.models import *

class Escola(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    local = models.CharField(db_column='Local', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Escola'

class Inscricao(models.Model):
    escola = models.ForeignKey(Escola, models.DO_NOTHING, db_column='escola')
    nalunos = models.IntegerField()
    ano = models.IntegerField()
    turma = models.CharField(max_length=255)
    areacientifica = models.CharField(max_length=255)
    participante = models.ForeignKey(Participante, models.DO_NOTHING, db_column='participante')
    diaaberto = models.ForeignKey(Diaaberto, models.DO_NOTHING, db_column='diaaberto')

    class Meta:
        managed = False
        db_table = 'Inscricao'


class Inscricaosessao(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricao')
    sessao = models.ForeignKey('atividades.Sessao, models.DO_NOTHING, db_column='sessao')
    nparticipantes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Inscricaosessao'


class Inscricaotransporte(models.Model):
    transporte = models.ForeignKey(Transporte, models.DO_NOTHING, db_column='transporte')
    npassageiros = models.IntegerField()
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricao')

    class Meta:
        managed = False
        db_table = 'Inscricaotransporte'


class Inscricaprato(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricao')
    prato = models.ForeignKey(Prato, models.DO_NOTHING, db_column='prato')
    campus = models.ForeignKey(Campus, models.DO_NOTHING, db_column='campus')
    npessoas = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Inscricaprato'

