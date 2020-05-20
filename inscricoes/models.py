from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime,time,timedelta

class Escola(models.Model):
    nome = models.CharField(max_length=200)
    local = models.CharField(max_length=128)

    class Meta:
        db_table = 'Escola'

class Inscricao(models.Model):
    nalunos = models.IntegerField()
    escola = models.ForeignKey(Escola, models.CASCADE)
    ano = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(12)
        ]
    )
    turma = models.CharField(max_length=1)
    areacientifica = models.CharField(max_length=64)
    # TODO: Descomentar quando a gestão de utilizadores estiver pronta
    # participante = models.ForeignKey(
    #     'utilizadores.Participante', models.CASCADE)
    # TODO: Descomentar quando a configuração do Dia Aberto estiver pronta
    # diaaberto = models.ForeignKey('configuracao.Diaaberto', models.CASCADE)

    class Meta:
        db_table = 'Inscricao'

    def get_dias(self):
        inscricao_sessoes= Inscricaosessao.objects.filter(inscricao=self)
        dias=[]
        for sessao in inscricao_sessoes:
            if sessao.sessao.dia not in dias:
                dias.append({'key':str(sessao.sessao.dia), 'value':sessao.sessao.dia})      
        return dias


    def get_horarios(self,dia):
        inscricao_sessoes = Inscricaosessao.objects.filter(inscricao=self).filter(sessao__dia=dia)
        horarios = []
        for sessao in inscricao_sessoes:
            if sessao.sessao.horarioid not in horarios:             
                horario = sessao.sessao.horarioid.inicio
                duracao = sessao.sessao.atividadeid.duracaoesperada*60
                td = (datetime.combine(datetime.min,horario) - datetime.min)
                secondsTotal = td.total_seconds() + duracao
                time = str(timedelta(seconds=secondsTotal))
                horarios.append({'key':sessao.sessao.horarioid.id, 'value':time})
        return horarios

    def get_origem(self,dia,horario_id):
        horario = 'configuracao.Horario'.objects.get(id=horario_id)
        inscricao_sessoes =  Inscricaosessao.objects.filter(inscricao=self).filter(sessao__dia=dia).filter(sessao__horarioid__inicio=horario.inicio)
        origem = []
        for local in inscricao_sessoes:
            origem.append({'key':local.sessao.atividadeid.espacoid.nome,'value':local.sessao.atividadeid.espacoid.nome})
        return origem
    
    def get_destino(self,dia,horario_id):
        horario = 'configuracao.Horario'.objects.get(id=horario_id)
        inscricao_sessoes =  Inscricaosessao.objects.filter(inscricao=self).filter(sessao__dia=dia).filter(sessao__horarioid__inicio=horario.fim)
        destino = []
        for local in inscricao_sessoes:
            destino.append({'key':local.sessao.atividadeid.espacoid.id,'value':local.sessao.atividadeid.espacoid.nome})
        return destino
        return


class Responsavel(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
    nome = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    tel = PhoneNumberField()

    class Meta:
        db_table = 'Responsavel'


class EscolaPortugal(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        db_table = 'EscolaPortugal'


class Inscricaoprato(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
    # TODO: Descomentar quando a configuração dos pratos estiver pronta
    # prato = models.ForeignKey('configuracao.Prato', models.CASCADE)
    campus = models.ForeignKey('configuracao.Campus', models.CASCADE)
    npessoas = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(300),
        ]
    )

    class Meta:
        db_table = 'InscricaoPrato'
        # TODO: Descomentar quando a configuração dos pratos estiver pronta
        # unique_together = (('inscricao', 'prato'),)


class Inscricaosessao(models.Model):
    inscricao = models.ForeignKey(
        Inscricao, models.CASCADE)
    sessao = models.ForeignKey(
        'atividades.Sessao', models.CASCADE)
    nparticipantes = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(300),
            # TODO: Adicionar validação de nparticipantes <= vagas na sessão
        ]
    )

    class Meta:
        db_table = 'InscricaoSessao'
        unique_together = (('inscricao', 'sessao'),)


class Inscricaotransporte(models.Model):
    inscricao = models.ForeignKey(
        Inscricao, models.CASCADE)
    transporte = models.ForeignKey('configuracao.Transporte', models.CASCADE)
    npassageiros = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(300),
            # TODO: Adicionar validação de npassageiros <= vagas no transporte
        ]
    )

    class Meta:
        db_table = 'InscricaoTransporte'
        unique_together = (('inscricao', 'transporte'),)
