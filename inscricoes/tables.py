import django_tables2 as tables
from .models import Inscricao, Escola
from configuracao.models import Diaaberto, Departamento, Unidadeorganica, Campus
from atividades.models import Atividade
import itertools
from django_tables2.utils import Accessor


class DepartamentoTable(tables.Table):
    #nome = tables.Column(verbose_name='Departamento')
    sigla = tables.Column(verbose_name='Departamento')
    class Meta:
        model = Departamento

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('unidadeorganicaid')
        self.columns.hide('nome')
        #self.columns.hide('atividadeid')


class InscricoesTable(tables.Table):
    
    Grupo = tables.Column('Grupo', accessor='id')
    #departamento = tables.Column(accessor='departamento.id')
    # dia = tables.Column()
    # hora = tables.Column()
    Turma = tables.Column(accessor='turma')
    Escola = tables.Column('Escola',accessor='escola.nome')
    nalunos = tables.Column(verbose_name='Nº Alunos')
    areacientifica = tables.Column(verbose_name='Área Científica')
    #participante = tables.Column(accessor='participante.nome')
    #NumDocentes = tables.Column('Nº Docentes', accessor='inscricao.nresponsaveis')
    #nome = tables.Column('Departamento',accessor='departamento.nome')
    
    class Meta:
        model = Inscricao
        sequence = ('Grupo', 'Escola', 'areacientifica', 'ano', 'Turma',  'nalunos')
        attrs = {"class": "paleblue"}
      
    def before_render(self, request):
        #self.columns.hide('areacientifica')
        self.columns.hide('id')
        self.columns.hide('escola')
        self.columns.hide('turma')
    




class DiaAbertoTable(tables.Table):
    datadiaabertoinicio = tables.DateColumn(verbose_name='Dia/Hora', format ='d/m/Y, h:i' )
    class Meta:
        model = Diaaberto
    
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('enderecopaginaweb')
        self.columns.hide('descricao')
        self.columns.hide('emaildiaaberto')
        self.columns.hide('ano')
        self.columns.hide('datainscricaoatividadesinicio')
        self.columns.hide('datapropostasatividadesincio')
        self.columns.hide('dataporpostaatividadesfim')
        self.columns.hide('administradorutilizadorid')
        self.columns.hide('datainscricaoatividadesfim')
        self.columns.hide('datadiaabertofim')
        self.columns.hide('precoalunos')
        self.columns.hide('precoprofessores')
        self.columns.hide('escalasessoes')
    

