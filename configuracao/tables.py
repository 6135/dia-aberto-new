import django_tables2 as tables
from configuracao.models import *
from django.utils.html import format_html
from django.db.models import Count
from atividades.models import Tema

class CursoTable(tables.Table):

    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    unidadeorganicaid = tables.Column('Faculdade')
    class Meta:
        model = Curso


    def before_render(self, request):
        self.columns.hide('id')
    
    def render_acoes(self,record):
        return format_html(f"""
            <div class="columns">
                <div class="column is-1">  
                    <a id='edit' href="{reverse('configuracao:editarCurso', kwargs={'id':record.pk})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                </div>
                &nbsp;
                <div class="column is-1">                 
                    <a onclick="alert.render('Tem a certeza que pretende eliminar este tema?','{reverse('configuracao:eliminarCurso', kwargs={'id':record.pk})}')">
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
                </div>
            </div> 
        """)

class TemaTable(tables.Table):

    activity_count = tables.Column('Atividades com o Tema', accessor='num_activities')
    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    class Meta:
        model = Tema


    def before_render(self, request):
        self.columns.hide('id')
    
    def order_activity_count(self, queryset, is_descending):
        queryset = queryset.annotate(count=Count('atividade')
        ).order_by(("" if is_descending else "-") + "count")
        return (queryset, True)

    def render_acoes(self,record):
        return format_html(f"""
            <div class="columns">
                <div class="column is-1">  
                    <a id='edit' href="{reverse('configuracao:editarTema', kwargs={'id':record.pk})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                </div>
                &nbsp;
                <div class="column is-1">                 
                    <a onclick="alert.render('Tem a certeza que pretende eliminar este tema?','{reverse('configuracao:eliminarTema', kwargs={'id':record.pk})}')">
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
                </div>
            </div> 
        """)

class DepartamentoTable(tables.Table):
    unidadeorganicaid = tables.Column('Unidade Organica')
    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    class Meta:
        model = Departamento


    def before_render(self, request):
        self.columns.hide('id')

    def render_acoes(self,record):
        print(record)
        return format_html(f"""
            <div class="columns">
                <div class="column is-1">  
                    <a id='edit' href="{reverse('configuracao:editarDepartamento', kwargs={'id':record.pk})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                </div>
                &nbsp;
                <div class="column is-1">                 
                    <a onclick="alert.render('Tem a certeza que pretende eliminar este tema?','{reverse('configuracao:eliminarDepartamento', kwargs={'id':record.pk})}')">
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
                </div>
            </div> 
        """)

class EdificioTable(tables.Table):

    numsalas = tables.Column('Numero de salas', accessor='count_salas')
    acoes = tables.Column('Operações', empty_values=())

    class Meta:
        model = Edificio

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('image')

    def render_nome(self,record):
        return format_html(str(Edificio.objects.get(id=record.pk)))

    def render_acoes(self,record):
        return format_html(f"""
            <div class="columns">
                <div class="column is-1">  
                    <a id='edit' href="{reverse('configuracao:editarEdificio', kwargs={'id':record.pk})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                </div>
                &nbsp;
                <div class="column is-1">                 
                    <a onclick="alert.render('Tem a certeza que pretende eliminar este tema?','{reverse('configuracao:eliminarEdificio', kwargs={'id':record.pk})}')">
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
                </div>
            </div> 
        """)


class UOTable(tables.Table):

    campusid = tables.Column('Campus')
    acoes = tables.Column('Operações', empty_values=())

    class Meta:
        model = Unidadeorganica

    def before_render(self, request):
        self.columns.hide('id')


    def render_acoes(self,record):
        return format_html(f"""
            <div class="columns">
                <div class="column is-1">  
                    <a id='edit' href="{reverse('configuracao:editarUO', kwargs={'id':record.pk})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                </div>
                &nbsp;
                <div class="column is-1">                 
                    <a onclick="alert.render('Tem a certeza que pretende eliminar este tema?','{reverse('configuracao:eliminarUO', kwargs={'id':record.pk})}')">
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
                </div>
            </div> 
        """)

class MenuTable(tables.Table):

    acoes = tables.Column('Operações', empty_values=())
    
    class Meta:
        model = Menu

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('horarioid')
        self.columns.hide('diaaberto')

    def render_acoes(self,record):
        return format_html(f"""
            <div class="columns">
                <div class="column is-1">  
                    <a id='edit' href="{reverse('configuracao:editarMenu', kwargs={'id':record.pk})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                </div>
                &nbsp;
                <div class="column is-1">                 
                    <a onclick="alert.render('Tem a certeza que pretende eliminar este tema?','{reverse('configuracao:eliminarMenu', kwargs={'id':record.pk})}')">
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
                </div>
            </div> 
        """)