from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField


class Inscricao(models.Model):
    nalunos = models.IntegerField()
    escola = models.ForeignKey('Escola', models.CASCADE)
    ano = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(12)
        ]
    )
    turma = models.CharField(max_length=1)
    areacientifica = models.CharField(max_length=64)
    participante = models.ForeignKey('utilizadores.Participante', models.CASCADE)
    diaaberto = models.ForeignKey('configuracao.Diaaberto', models.CASCADE)

    class Meta:
        db_table = 'Inscricao'


class Responsavel(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
    nome = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    tel = PhoneNumberField()

    class Meta:
        db_table = 'Responsavel'


class Escola(models.Model):
    nome = models.CharField(max_length=200)
    local = models.CharField(max_length=128)

    class Meta:
        db_table = 'Escola'


class EscolaPortugal(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        db_table = 'EscolaPortugal'


class Inscricaoprato(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
    prato = models.ForeignKey('configuracao.Prato', models.CASCADE)
    campus = models.ForeignKey('configuracao.Campus', models.CASCADE)
    npessoas = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(300),
        ]
    )

    class Meta:
        db_table = 'InscricaoPrato'
        unique_together = (('inscricao', 'prato'),)


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
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
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