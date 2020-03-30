# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrador(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Administrador'


class Anfiteatro(models.Model):
    espacoid = models.OneToOneField('Espaco', models.DO_NOTHING, db_column='EspacoID', primary_key=True)  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Anfiteatro'


class Arlivre(models.Model):
    espacoid = models.OneToOneField('Espaco', models.DO_NOTHING, db_column='EspacoID', primary_key=True)  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ArLivre'


class Atividade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase.
    publicoalvo = models.CharField(db_column='Publicoalvo', max_length=255)  # Field name made lowercase.
    nrcolaboradoresnecessario = models.IntegerField(db_column='nrColaboradoresNecessario')  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=64)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=64)  # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey('Coordenador', models.DO_NOTHING, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    professoruniversitarioutilizadorid = models.ForeignKey('Professoruniversitario', models.DO_NOTHING, db_column='ProfessorUniversitarioUtilizadorID')  # Field name made lowercase.
    datasubmissao = models.DateTimeField(db_column='dataSubmissao')  # Field name made lowercase.
    dataalteracao = models.DateTimeField(db_column='dataAlteracao')  # Field name made lowercase.
    duracaoesperada = models.IntegerField(db_column='duracaoEsperada')  # Field name made lowercase.
    participantesmaximo = models.IntegerField(db_column='participantesMaximo')  # Field name made lowercase.
    diaabertoid = models.ForeignKey('Diaaberto', models.DO_NOTHING, db_column='diaAbertoID')  # Field name made lowercase.
    espacoid = models.ForeignKey('Espaco', models.DO_NOTHING, db_column='EspacoID')  # Field name made lowercase.
    tema = models.ForeignKey('Tema', models.DO_NOTHING, db_column='Tema', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Atividade'


class Campus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    menuid = models.ForeignKey('Menu', models.DO_NOTHING, db_column='MenuID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Campus'


class Colaborador(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    curso = models.CharField(db_column='Curso', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Colaborador'


class Colaboradorhorario(models.Model):
    colaboradorutilizadorid = models.OneToOneField(Colaborador, models.DO_NOTHING, db_column='ColaboradorUtilizadorID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey('Horario', models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    horarioinicio = models.DateField(db_column='HorarioInicio')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ColaboradorHorario'
        unique_together = (('colaboradorutilizadorid', 'horarioid', 'horarioinicio'),)


class Coordenador(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=True, null=True)  # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='unidadeOrganicaID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Coordenador'


class Departamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='UnidadeOrganicaID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departamento'


class Diaaberto(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    enderecopaginaweb = models.CharField(db_column='EnderecoPaginaWeb', max_length=255)  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase.
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


class Envionotificacao(models.Model):
    notificacaoid = models.OneToOneField('Notificacao', models.DO_NOTHING, db_column='NotificacaoID', primary_key=True)  # Field name made lowercase.
    utilizadorid = models.ForeignKey('Utilizador', models.DO_NOTHING, db_column='UtilizadorID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EnvioNotificacao'
        unique_together = (('notificacaoid', 'utilizadorid'),)


class Escola(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    local = models.CharField(db_column='Local', max_length=255)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=16)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Escola'


class Espaco(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    edificio = models.CharField(db_column='Edificio', max_length=255, blank=True, null=True)  # Field name made lowercase.
    andar = models.CharField(db_column='Andar', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Espaco'


class Horario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    inicio = models.TimeField(db_column='Inicio')  # Field name made lowercase.
    fim = models.TimeField(db_column='Fim')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Horario'


class Idioma(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    diaabertoid = models.ForeignKey(Diaaberto, models.DO_NOTHING, db_column='DiaAbertoID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Idioma'


class Inscricao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nrinscricao = models.IntegerField(db_column='NrInscricao')  # Field name made lowercase.
    ano = models.IntegerField(db_column='Ano')  # Field name made lowercase.
    local = models.CharField(db_column='Local', max_length=128)  # Field name made lowercase.
    areacientifica = models.CharField(db_column='AreaCientifica', max_length=64)  # Field name made lowercase.
    participanteutilizadorid = models.ForeignKey('Participante', models.DO_NOTHING, db_column='ParticipanteUtilizadorID')  # Field name made lowercase.
    diaabertoid = models.ForeignKey(Diaaberto, models.DO_NOTHING, db_column='DiaAbertoID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Inscricao'


class Inscricaocoletiva(models.Model):
    inscricaoid = models.OneToOneField(Inscricao, models.DO_NOTHING, db_column='InscricaoID', primary_key=True)  # Field name made lowercase.
    escolaid = models.ForeignKey(Escola, models.DO_NOTHING, db_column='EscolaID')  # Field name made lowercase.
    nralunos = models.IntegerField(db_column='nrAlunos')  # Field name made lowercase.
    nresponsaveis = models.IntegerField(db_column='nResponsaveis')  # Field name made lowercase.
    turma = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'InscricaoColetiva'
        unique_together = (('inscricaoid', 'escolaid'),)


class Inscricaoindividual(models.Model):
    inscricaoid = models.OneToOneField(Inscricao, models.DO_NOTHING, db_column='InscricaoID', primary_key=True)  # Field name made lowercase.
    nracompanhantes = models.IntegerField(db_column='nrAcompanhantes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InscricaoIndividual'


class Inscricaoprato(models.Model):
    inscricaoid = models.OneToOneField(Inscricao, models.DO_NOTHING, db_column='InscricaoID', primary_key=True)  # Field name made lowercase.
    pratoid = models.ForeignKey('Prato', models.DO_NOTHING, db_column='PratoID')  # Field name made lowercase.
    nrpessoas = models.IntegerField(db_column='NrPessoas')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InscricaoPrato'
        unique_together = (('inscricaoid', 'pratoid'),)


class Inscricaosessao(models.Model):
    inscricaoid = models.OneToOneField(Inscricao, models.DO_NOTHING, db_column='InscricaoID', primary_key=True)  # Field name made lowercase.
    sessaoid = models.ForeignKey('Sessao', models.DO_NOTHING, db_column='SessaoID')  # Field name made lowercase.
    nrparticipantes = models.IntegerField(db_column='nrParticipantes')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InscricaoSessao'
        unique_together = (('inscricaoid', 'sessaoid'),)


class Inscricaotransporte(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    inscricaoid = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='InscricaoID')  # Field name made lowercase.
    transporteid = models.ForeignKey('Transporte', models.DO_NOTHING, db_column='TransporteID')  # Field name made lowercase.
    nrparticipantes = models.IntegerField(db_column='NrParticipantes')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InscricaoTransporte'


class Materiais(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    atividadeid = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Materiais'


class Menu(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey(Horario, models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    precoalunos = models.FloatField(db_column='PrecoAlunos')  # Field name made lowercase.
    precoprofessores = models.FloatField(db_column='PrecoProfessores', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Menu'


class Notificacao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null=True)  # Field name made lowercase.
    criadoem = models.CharField(db_column='CriadoEm', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Notificacao'


class Participante(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Participante'


class Prato(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nrpratosdisponiveis = models.IntegerField(db_column='NrPratosDisponiveis')  # Field name made lowercase.
    prato = models.IntegerField(db_column='Prato')  # Field name made lowercase.
    menuid = models.ForeignKey(Menu, models.DO_NOTHING, db_column='MenuID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prato'


class Professoruniversitario(models.Model):
    utilizadorid = models.OneToOneField('Utilizador', models.DO_NOTHING, db_column='UtilizadorID', primary_key=True)  # Field name made lowercase.
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=True, null=True)  # Field name made lowercase.
    departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='departamento')

    class Meta:
        managed = False
        db_table = 'ProfessorUniversitario'


class Recepcaonotificacao(models.Model):
    notificacaoid = models.OneToOneField(Notificacao, models.DO_NOTHING, db_column='NotificacaoID', primary_key=True)  # Field name made lowercase.
    utilizadorid = models.ForeignKey('Utilizador', models.DO_NOTHING, db_column='UtilizadorID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RecepcaoNotificacao'
        unique_together = (('notificacaoid', 'utilizadorid'),)


class Sala(models.Model):
    espacoid = models.ForeignKey(Espaco, models.DO_NOTHING, db_column='EspacoID')  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sala'


class Sessao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey(Horario, models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    ninscritos = models.IntegerField(db_column='NInscritos')  # Field name made lowercase.
    vagas = models.IntegerField(db_column='Vagas')  # Field name made lowercase.
    atividadeid = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sessao'


class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    concluida = models.IntegerField(db_column='Concluida')  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)  # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey(Coordenador, models.DO_NOTHING, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    colaboradorutilizadorid = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='ColaboradorUtilizadorID')  # Field name made lowercase.
    atividadeid = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tarefa'


class Tema(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tema = models.CharField(db_column='Tema', max_length=64)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tema'


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


class Unidadeorganica(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=255)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnidadeOrganica'


class Utilizador(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Utilizador'
