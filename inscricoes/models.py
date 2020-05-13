from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField
from configuracao.models import *
from colaboradores.models import *
from utilizadores.models import *
from datetime import datetime,time,timedelta
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
    horariochegada = models.TimeField(blank=True, null=True)
    horariopartida = models.TimeField(blank=True, null=True)
    localchegada = models.CharField(db_column='Localchegada', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Inscricao'

    def get_dias(self):
        inscricao_sessoes= Inscricaosessao.objects.filter(inscricao=self)
        dias=[]
        for sessao in inscricao_sessoes:
            if sessao.sessao.dia not in dias:
                dias.append({'key':str(sessao.sessao.dia), 'value':sessao.sessao.dia})      
        return dias

    def get_horarios(self,dia):
        inscricao_sessoes= Inscricaosessao.objects.filter(inscricao=self)
        horarios=[]
        for sessao in inscricao_sessoes:
            if sessao.sessao.horarioid not in horarios:             
                horario = sessao.sessao.horarioid.inicio
                duracao = sessao.sessao.atividadeid.duracaoesperada*60
                td = (datetime.combine(datetime.min,horario) - datetime.min)
                secondsTotal = td.total_seconds() + duracao
                time = str(timedelta(seconds=secondsTotal))
                horarios.append({'key':sessao.sessao.horarioid.id, 'value':time})
        return horarios

    def get_locais(self):
        locais 



class Inscricaosessao(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='inscricao')
    sessao = models.ForeignKey('atividades.Sessao', models.DO_NOTHING, db_column='sessao')
    nparticipantes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Inscricaosessao'


class Inscricaotransporte(models.Model):
    transporte = models.ForeignKey(Transportehorario, models.DO_NOTHING, db_column='transporte')
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

