from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField


class Inscricao(models.Model):
    ninscricao = models.IntegerField()
    ano = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(12)
        ]
    )
    local = models.CharField(max_length=128)
    areacientifica = models.CharField(max_length=64)
    participante = models.ForeignKey(
        'utilizadores.Participante', models.CASCADE)
    # TODO: Descomentar quando a configuração do Dia Aberto estiver pronta
    # diaaberto = models.ForeignKey('configuracao.Diaaberto', models.CASCADE)

    class Meta:
        db_table = 'Inscricao'


class Escola(models.Model):
    nome = models.CharField(max_length=128)
    local = models.CharField(max_length=128)
    telefone = PhoneNumberField()
    email = models.EmailField()

    class Meta:
        db_table = 'Escola'


class Inscricaocoletiva(Inscricao):
    escola = models.ForeignKey(Escola, models.CASCADE)
    nalunos = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(300)
        ]
    )
    nresponsaveis = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(20)
        ]
    )
    turma = models.CharField(max_length=255)

    class Meta:
        db_table = 'InscricaoColetiva'


class Inscricaoindividual(Inscricao):
    nacompanhantes = models.IntegerField(
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(20)
        ]
    )

    class Meta:
        db_table = 'InscricaoIndividual'


class Inscricaoprato(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
    prato = models.ForeignKey('configuracao.Prato', models.CASCADE)
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
        Inscricao, models.CASCADE, db_column='InscricaoID')
    sessao = models.ForeignKey(
        'atividades.Sessao', models.CASCADE, db_column='SessaoID')
    nparticipantes = models.IntegerField(db_column='nrParticipantes',
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(300),
            # TODO: Adicionar validação de nparticipantes <= vagas na sessão
        ]
    )

    class Meta:
        db_table = 'InscricaoSessao'


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
