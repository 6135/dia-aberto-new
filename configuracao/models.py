# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Transporte(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    identificador = models.IntegerField(db_column='Identificador')

    class Meta:
        db_table = 'Transporte'


class Transportehorario(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    origem = models.IntegerField(db_column='Origem')
    # Field name made lowercase.
    chegada = models.IntegerField(db_column='Chegada')
    # Field name made lowercase.
    horarioid = models.ForeignKey(
        'Horario', models.CASCADE, db_column='HorarioID')
    # Field name made lowercase.
    transporteid = models.ForeignKey(
        Transporte, models.CASCADE, db_column='TransporteID')

    class Meta:
        db_table = 'TransporteHorario'


class Transportepessoal(models.Model):
    # Field name made lowercase.
    transporteid = models.OneToOneField(
        Transporte, models.CASCADE, db_column='TransporteID', primary_key=True)
    # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=255)

    class Meta:
        db_table = 'TransportePessoal'


class Transporteuniversitario(models.Model):
    # Field name made lowercase.
    transporteid = models.OneToOneField(
        Transporte, models.CASCADE, db_column='TransporteID', primary_key=True)
    # Field name made lowercase.
    capacidade = models.IntegerField(db_column='Capacidade')

    class Meta:
        db_table = 'TransporteUniversitario'


class Diaaberto(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    enderecopaginaweb = models.CharField(
        db_column='EnderecoPaginaWeb', max_length=255)
    # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')
    # Field name made lowercase.
    emaildiaaberto = models.CharField(
        db_column='EmailDiaAberto', max_length=255)
    ano = models.IntegerField(db_column='Ano')  # Field name made lowercase.
    # Field name made lowercase.
    datadiaabertoinicio = models.DateTimeField(db_column='DataDiaAbertoInicio')
    # Field name made lowercase.
    datadiaabertofim = models.DateTimeField(db_column='DataDiaAbertoFim')
    datainscricaoatividadesinicio = models.DateTimeField(
        db_column='DataInscricaoAtividadesInicio')  # Field name made lowercase.
    # Field name made lowercase.
    datainscricaoatividadesfim = models.DateTimeField(
        db_column='DataInscricaoAtividadesFim')
    # Field name made lowercase.
    datapropostasatividadesincio = models.DateTimeField(
        db_column='DataPropostasAtividadesIncio')
    # Field name made lowercase.
    dataporpostaatividadesfim = models.DateTimeField(
        db_column='DataPorpostaAtividadesFim')
    # Field name made lowercase.
    administradorutilizadorid = models.ForeignKey(
        'utilizadores.Administrador', models.CASCADE, db_column='AdministradorUtilizadorID')

    class Meta:
        db_table = 'DiaAberto'


class Menu(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    horarioid = models.ForeignKey(
        'Horario', models.CASCADE, db_column='HorarioID')
    # Field name made lowercase.
    utilizadorid = models.ForeignKey(
        'utilizadores.Utilizador', models.CASCADE, db_column='UtilizadorID')
    # Field name made lowercase.
    precoalunos = models.FloatField(db_column='PrecoAlunos')
    # Field name made lowercase.
    precoprofessores = models.FloatField(
        db_column='PrecoProfessores', blank=True, null=True)
    # Field name made lowercase.
    tipo = models.CharField(
        db_column='Tipo', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    menu = models.IntegerField(db_column='Menu', blank=True, null=True)
    # Field name made lowercase.
    horarioinicio = models.DateField(
        db_column='HorarioInicio', blank=True, null=True)

    class Meta:
        db_table = 'Menu'


class Prato(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nrpratosdisponiveis = models.IntegerField(db_column='NrPratosDisponiveis')
    # Field name made lowercase.
    prato = models.IntegerField(db_column='Prato')
    # Field name made lowercase.
    menuid = models.ForeignKey(Menu, models.CASCADE, db_column='MenuID')

    class Meta:
        db_table = 'Prato'


class Campus(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    menuid = models.ForeignKey(Menu, models.CASCADE, db_column='MenuID')
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Campus'


class Departamento(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    atividadeid = models.ForeignKey(
        'atividades.Atividade', models.CASCADE, db_column='AtividadeID')
    # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey(
        'Unidadeorganica', models.CASCADE, db_column='UnidadeOrganicaID')
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Departamento'


class Sala(models.Model):
    # Field name made lowercase.
    espacoid = models.ForeignKey(
        'atividades.Espaco', models.CASCADE, db_column='EspacoID')
    # Field name made lowercase.
    espacoedificio = models.CharField(
        db_column='EspacoEdificio', max_length=255)

    class Meta:
        db_table = 'Sala'


class Idioma(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    diaabertoid = models.ForeignKey(
        Diaaberto, models.CASCADE, db_column='DiaAbertoID')
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    sigla = models.CharField(
        db_column='Sigla', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Idioma'


class Horario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    inicio = models.TimeField(db_column='Inicio')  # Field name made lowercase.
    fim = models.TimeField(db_column='Fim')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Horario'

        
class Unidadeorganica(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=255)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnidadeOrganica'
