from django.db import models
from utilizadores.models import *
from coordenadores.models import *
from configuracao.models import *
from inscricoes.models import *
from notificacoes.models import *

from utilizadores.models import *
from coordenadores.models import *
from configuracao.models import *
from inscricoes.models import *
from notificacoes.models import *

# class Atividade(models.Model):
#     nome = models.CharField(max_length=255)
#     descricao = models.TextField()
#     capacidademaxima = models.IntegerField()
#     duracao = models.IntegerField()
#     publicoalvo = models.CharField(max_length=255)
#     coordenador = models.ForeignKey(
#         'utilizadores.Coordenador', models.CASCADE)
#     professoruniversitario = models.ForeignKey(
#         'utilizadores.Professoruniversitario', models.CASCADE)
#     ncolaboradoresnecessarios = models.IntegerField()
#     datasubmissao = models.DateField(auto_now_add=True)
#     estado = models.CharField(max_length=255)
#     tipo = models.CharField(max_length=255)

#     departamentoid = models.ForeignKey(
#         'configuracao.Departamento', models.CASCADE, db_column='departamentoID')


#     class Meta:
#         db_table = 'Atividade'


class Atividade(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)
    # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')
    publicosalvo = (("Ciencias e Tecnologia", "Ciências e Tecnologia"),
                    ("Linguas e Humanidades", "Linguas e Humanidades"), ("Economia", "Economia"))
    # Field name made lowercase.
    publicoalvo = models.CharField(
        db_column='Publicoalvo', max_length=255, choices=publicosalvo, default='')
    # Field name made lowercase.
    nrcolaboradoresnecessario = models.IntegerField(
        db_column='nrColaboradoresNecessario')
    tipos = (("Atividade Laboratorial", "Atividade Laboratorial"),
             ("Tertulia", "Tertulia"), ("Palestra", "Palestra"))
    # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=64,
                            choices=tipos, default='Palestra')
    # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=64)
    # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey(
        Coordenador, models.CASCADE, db_column='CoordenadorUtilizadorID')
    professoruniversitarioutilizadorid = models.ForeignKey(
        ProfessorUniversitario, models.CASCADE, db_column='ProfessorUniversitarioUtilizadorID')  # Field name made lowercase.
    # Field name made lowercase.
    datasubmissao = models.DateTimeField(
        db_column='dataSubmissao', auto_now_add=True)
    # Field name made lowercase.
    dataalteracao = models.DateTimeField(
        db_column='dataAlteracao', auto_now=True)
    # Field name made lowercase.
    duracaoesperada = models.IntegerField(db_column='duracaoEsperada')
    # Field name made lowercase.
    participantesmaximo = models.IntegerField(db_column='participantesMaximo')
    # Field name made lowercase.
    diaabertoid = models.ForeignKey(
        Diaaberto, models.CASCADE, db_column='diaAbertoID')
    # Field name made lowercase.
    espacoid = models.ForeignKey(Espaco, models.CASCADE, db_column='EspacoID')
    # Field name made lowercase.
    tema = models.ForeignKey('Tema', models.CASCADE,
                             db_column='Tema', blank=False, null=False)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Atividade._meta.fields]


class Sessao(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    horarioid = models.ForeignKey(
        Horario, models.DO_NOTHING, db_column='HorarioID')
    # Field name made lowercase.
    ninscritos = models.IntegerField(db_column='NInscritos')
    # Field name made lowercase.
    vagas = models.IntegerField(db_column='Vagas')
    # Field name made lowercase.
    atividadeid = models.ForeignKey(
        Atividade, models.DO_NOTHING, db_column='AtividadeID')
    # Field name made lowercase.
    dia = models.DateField(db_column='Dia', blank=True, null=True)

    def timeRange_(self, seperator=' até '):
        return self.horarioid.inicio.strftime('%H:%M') + str(seperator) + self.horarioid.fim.strftime('%H:%M')

    class Meta:
        db_table = 'ArLivre'


class Materiais(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    atividadeid = models.ForeignKey(
        Atividade, models.DO_NOTHING, db_column='AtividadeID')
    nomematerial = models.CharField(
        db_column='nome', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Materiais'


class Sessao(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    horarioid = models.ForeignKey(
        Horario, models.DO_NOTHING, db_column='HorarioID')
    # Field name made lowercase.
    ninscritos = models.IntegerField(db_column='NInscritos')
    # Field name made lowercase.
    vagas = models.IntegerField(db_column='Vagas')
    # Field name made lowercase.
    atividadeid = models.ForeignKey(
        Atividade, models.DO_NOTHING, 'sessoes', db_column='AtividadeID')
    # Field name made lowercase.
    dia = models.DateField(db_column='Dia', blank=True, null=True)

    class Meta:
        db_table = 'Sessao'


class Tema(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    tema = models.CharField(db_column='Tema', max_length=64)

    class Meta:
        db_table = 'ArLivre'


class Tema(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    tema = models.CharField(db_column='Tema', max_length=64)

    class Meta:
        db_table = 'Tema'
