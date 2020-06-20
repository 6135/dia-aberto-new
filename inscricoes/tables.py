import django_tables2 as tables
from .models import Inscricao, Escola
from configuracao.models import Diaaberto, Departamento, Unidadeorganica, Campus
from atividades.models import Atividade
import itertools
from django.utils.html import format_html
from django.urls import reverse


class DepartamentoTable(tables.Table):
    #nome = tables.Column(verbose_name='Departamento')
    sigla = tables.Column(verbose_name='Departamento')

    class Meta:
        model = Departamento

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('unidadeorganicaid')
        self.columns.hide('nome')
        # self.columns.hide('atividadeid')


class InscricoesTable(tables.Table):
    grupo = tables.Column('Grupo', accessor='id')
    #departamento = tables.Column(accessor='departamento__id')
    # dia = tables.Column()
    # hora = tables.Column()
    nalunos = tables.Column(verbose_name='Qtd', attrs={
                            "abbr": {"title": "Quantidade"}})
    #participante = tables.Column(accessor='participante.nome')
    #NumDocentes = tables.Column('Nº Docentes', accessor='inscricao.nresponsaveis')
    #nome = tables.Column('Departamento',accessor='departamento.nome')
    acoes = tables.Column('Ações', empty_values=(),
                          orderable=False, attrs={"td": {"style": "min-width: 104px;"}})
    turma = tables.Column(empty_values=())

    class Meta:
        model = Inscricao
        sequence = ('grupo', 'dia', 'escola', 'areacientifica',
                    'turma', 'nalunos', 'acoes')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('ano')
        self.columns.hide('areacientifica')
        self.columns.hide('participante')
        self.columns.hide('diaaberto')
        self.columns.hide('meio_transporte')
        self.columns.hide('hora_chegada')
        self.columns.hide('local_chegada')
        self.columns.hide('entrecampi')
        self.columns.hide('individual')

    def render_acoes(self, record):
        return format_html(f"""
        <div>
            <a href='{reverse("inscricoes:consultar-inscricao", kwargs={"pk": record.pk, "step": 5})}'>
                <span class="icon has-text-info">
                    <i class="mdi mdi-eye mdi-24px"></i>
                </span>
            </a>
            <a href='{reverse("inscricoes:consultar-inscricao", kwargs={"pk": record.pk})}'>
                <span class="icon has-text-warning">
                    <i class="mdi mdi-pencil mdi-24px"></i>
                </span>
            </a>
            <a onclick="alert.render('Tem a certeza que pretende eliminar esta inscrição?','{reverse("inscricoes:apagar-inscricao", kwargs={"pk": record.pk})}')">
                <span class="icon has-text-danger">
                    <i class="mdi mdi-close-box mdi-24px"></i>
                </span>
            </a>
        </div>
        """)

    def render_participante(self, value):
        return format_html(f"{value.first_name} {value.last_name}")

    def render_turma(self, value, record):
        if not record.ano:
            return format_html("(Individual)")
        return format_html(f"{record.ano}º {value}, {record.areacientifica}")


class DiaAbertoTable(tables.Table):
    datadiaabertoinicio = tables.DateColumn(
        verbose_name='Dia/Hora', format='d/m/Y, h:i')

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
