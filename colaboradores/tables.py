import django_tables2 as django_tables
from coordenadores.models import Tarefa
from django.utils.html import format_html


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
