# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from utilizadores.models import Administrador
from atividades.models import Espaco


class Transporte(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    identificador = models.IntegerField(db_column='Identificador')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transporte'

class Transportehorario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    origem = models.IntegerField(db_column='Origem')  # Field name made lowercase.
    chegada = models.IntegerField(db_column='Chegada')  # Field name made lowercase.
    horarioid = models.ForeignKey(Horario, models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    transporteid = models.ForeignKey(Transporte, models.DO_NOTHING, db_column='TransporteID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransporteHorario'


class Transportepessoal(models.Model):
    transporteid = models.OneToOneField(Transporte, models.DO_NOTHING, db_column='TransporteID', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransportePessoal'



class Transporteuniversitario(models.Model):
    transporteid = models.OneToOneField(Transporte, models.DO_NOTHING, db_column='TransporteID', primary_key=True)  # Field name made lowercase.
    capacidade = models.IntegerField(db_column='Capacidade')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransporteUniversitario'

class Diaaberto(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    enderecopaginaweb = models.CharField(db_column='EnderecoPaginaWeb', max_length=255)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)  # Field name made lowercase.
    emaildiaaberto = models.CharField(db_column='EmailDiaAberto', max_length=255)  # Field name made lowercase.
    ano = models.IntegerField(db_column='Ano')  # Field name made lowercase.
    datadiaabertoinicio = models.DateTimeField(db_column='DataDiaAbertoInicio')  # Field name made lowercase.
    datadiaabertofim = models.DateTimeField(db_column='DataDiaAbertoFim')  # Field name made lowercase.
    datainscricaoatividadesinicio = models.DateTimeField(db_column='DataInscricaoAtividadesInicio')  # Field name made lowercase.
    datainscricaoatividadesfim = models.DateTimeField(db_column='DataInscricaoAtividadesFim')  # Field name made lowercase.
    datapropostasatividadesincio = models.DateTimeField(db_column='DataPropostasAtividadesIncio')  # Field name made lowercase.
    dataporpostaatividadesfim = models.DateTimeField(db_column='DataPorpostaAtividadesFim')  # Field name made lowercase.
    administradorutilizadorid = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='AdministradorUtilizadorID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DiaAberto'


class Menu(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey(Horario, models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    precoalunos = models.FloatField(db_column='PrecoAlunos')  # Field name made lowercase.
    precoprofessores = models.FloatField(db_column='PrecoProfessores', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Menu'


class Prato(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nrpratosdisponiveis = models.IntegerField(db_column='NrPratosDisponiveis')  # Field name made lowercase.
    prato = models.IntegerField(db_column='Prato')  # Field name made lowercase.
    menuid = models.ForeignKey(Menu, models.DO_NOTHING, db_column='MenuID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prato'

class Campus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    menuid = models.ForeignKey('Menu', models.DO_NOTHING, db_column='MenuID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Campus'


class Departamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='UnidadeOrganicaID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departamento'



class Sala(models.Model):
    espacoid = models.ForeignKey(Espaco, models.DO_NOTHING, db_column='EspacoID')  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sala'


class Idioma(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    diaabertoid = models.ForeignKey(Diaaberto, models.DO_NOTHING, db_column='DiaAbertoID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Idioma'

class Horario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    inicio = models.TimeField(db_column='Inicio')  # Field name made lowercase.
    fim = models.TimeField(db_column='Fim')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Horario'