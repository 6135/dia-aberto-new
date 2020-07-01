import django_tables2 as django_tables
from coordenadores.models import Tarefa
from django.utils.html import format_html
from atividades.models import *


class TarefasTable(django_tables.Table):

    tipo = django_tables.Column(accessor='tipo', orderable=False)

    class Meta:
        model = Tarefa
        sequence = ('nome', 'dia', 'horario', 'tipo', 'estado')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('coord')
        self.columns.hide('colab')
        self.columns.hide('created_at')
        return super().before_render(request)

    def render_tipo(self, value):
        if value == 'tarefaAuxiliar':
            return "Ajudar na Atividade"
        elif value == 'tarefaAcompanhar':
            return "Acompanhar Participantes"
        else:
            return "Outras Tarefas"

    def render_estado(self, value):
        estado = ""
        cor = ""
        if(value == 'naoConcluida'):
            estado = "Não Concluída"
            cor = "warning"
        elif(value == 'Concluida'):
            estado = "Concluida"
            cor = "success"
        elif(value == 'Cancelada'):
            estado = "Cancelada"
            cor = "danger"
        elif(value == 'Iniciada'):
            estado = "Iniciada"
            cor = "info"
        return format_html(f"""
            <span class="tag is-{cor}" style="width: 10rem;font-size: small;">{estado}</span>
        """)





class ColaboradorAtividadesTable(django_tables.Table):
    
    acoes = django_tables.Column('Ações', empty_values=())
    professoruniversitarioutilizadorid = django_tables.Column('Professor')
    datasubmissao = django_tables.Column('Data de Submissão')
    class Meta:
        model = Atividade
        sequence = ('nome','professoruniversitarioutilizadorid','tipo','tema', 'acoes')
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('nrcolaboradoresnecessario')
        self.columns.hide('publicoalvo')
        self.columns.hide('dataalteracao')
        self.columns.hide('duracaoesperada')
        self.columns.hide('participantesmaximo')
        self.columns.hide('espacoid')
        self.columns.hide('diaabertoid')
        self.columns.hide('estado')
        self.columns.hide('datasubmissao')


    def render_professoruniversitarioutilizadorid(self,record):
        return str(record.professoruniversitarioutilizadorid.full_name)

    def render_tema(self,record):
        return str(record.tema.tema)    
    
    def render_acoes(self,record):
        return format_html(f"""
            <div>
                <a id='edit' href="{reverse('colaboradores:selecionar-atividade', kwargs={'id':record.pk})}">
                    
                        <span class="icon is-small" style="margin-left:18%">
                        <div data-tooltip="Escolher Atividade">
                            <i class="mdi mdi-calendar-check mdi-24px"></i>
                            </div> 
                        </span>
                       
                </a>
            </div> 
        """)
