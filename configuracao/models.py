
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
    choices = {
        ('Penha','Penha'),
        ('Terminal','Terminal'),
        ('Gambelas','Gambelas'),
    }
    origem = models.CharField(db_column='Origem', max_length=32, blank=True, null=False, choices=choices)
    # Field name made lowercase.
    chegada = models.CharField(db_column='Chegada', max_length=32, blank=True, null=False, choices=choices)
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
    precoalunos = models.FloatField(db_column='PrecoAlunos')
    # Field name made lowercase.
    precoprofessores = models.FloatField(
        db_column='PrecoProfessores', blank=True, null=True)
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

    def days_as_dict(self):
        data_inicio = self.datadiaabertoinicio
        data_fim = self.datadiaabertofim
        total_dias = data_fim-data_inicio+timedelta(days=1)
        return [{
            'key':	str((data_inicio+timedelta(days=d)).date()),
            'value':	str((data_inicio+timedelta(days=d)).date())
        } for d in range(total_dias.days)
        ]

    def days_as_tuples(self):
        data_inicio = self.datadiaabertoinicio
        data_fim = self.datadiaabertofim
        total_dias = data_fim-data_inicio+timedelta(days=1)
        return [(
            str((data_inicio+timedelta(days=d)).date()),
            str((data_inicio+timedelta(days=d)).date())
        ) for d in range(total_dias.days)
        ]

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
    campusid = models.ForeignKey(
        'Campus', models.CASCADE, db_column='CampusID')
    # Field name made lowercase.
    horarioinicio = models.DateField(
        db_column='HorarioInicio', blank=True, null=True)

    class Meta:
        db_table = 'Menu'


class Campus(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    # TODO: Porque é que o campus tem um menuid?
    # menuid = models.ForeignKey(Menu, models.CASCADE, db_column='MenuID')
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Campus'


class Prato(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    prato = models.IntegerField(db_column='Prato')
    # Field name made lowercase.
    menuid = models.ForeignKey(Menu, models.CASCADE, db_column='MenuID')

    class Meta:
        db_table = 'Prato'


class Departamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    sigla = models.CharField(
        db_column='Sigla', max_length=255, blank=True, null=True)
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)
    unidadeorganicaid = models.ForeignKey(
        'Unidadeorganica', models.CASCADE, db_column='UnidadeorganicaID')

    class Meta:
        db_table = 'Departamento'

    def __str__(self):
        return self.nome


class Curso(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)

    sigla = models.CharField(
        db_column='Sigla', max_length=255, blank=True, null=True)

    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)

    unidadeorganicaid = models.ForeignKey(
        'Unidadeorganica', models.CASCADE, db_column='UnidadeorganicaID')

    class Meta:
        db_table = 'Curso'

    def __str__(self):
        return self.nome


class Unidadeorganica(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    sigla = models.CharField(
        db_column='Sigla', max_length=255, blank=True, null=False)
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=False)
    campus = models.ForeignKey('Campus', models.CASCADE)

    class Meta:
        db_table = 'UnidadeOrganica'

    def __str__(self):
        return self.nome


class Sala(models.Model):
    # Field name made lowercase.
    espacoid = models.ForeignKey(
        'Espaco', models.CASCADE, db_column='EspacoID')
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
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    inicio = models.TimeField(db_column='Inicio')  # Field name made lowercase.
    fim = models.TimeField(db_column='Fim')  # Field name made lowercase.

    class Meta:
        db_table = 'Horario'


class Espaco(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    edificio = models.ForeignKey(
        'Edificio', models.DO_NOTHING, db_column='Edificio', blank=True, null=True)
    # Field name made lowercase.
    andar = models.CharField(
        db_column='Andar', max_length=255, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=255)

    class Meta:
        db_table = 'Espaco'


class Edificio(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=32)
    # Field name made lowercase.
    campus = models.ForeignKey('Campus', models.DO_NOTHING, db_column='Campus')

    class Meta:
        db_table = 'Edificio'
