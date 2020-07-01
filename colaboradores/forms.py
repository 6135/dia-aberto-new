from django.forms import ModelForm
from .models import *
from utilizadores.models import *
from coordenadores.models import *
from django.forms import *
from django import forms


TIPO = (
    ("Tarefa", "Todos os Tipos"),
    ("tarefaAuxiliar", "Ajudar na Atividade"),
    ("tarefaAcompanhar", "Acompanhar Participantes"),
    ("tarefaOutra", "Outras Tarefas"),
)

ESTADOS = (
    ("", "Todos os Estados"),
    ("Concluida", "Concluída"),
    ("naoConcluida", "Não Concluída"),
    ("Iniciada", "Iniciada"),
    ("Cancelada", "Cancelada"),
)




class TarefaFiltro(Form):
    filtro_tipo = ChoiceField(
        choices=TIPO,
        widget=Select(),
        required=False,
    )

    filtro_estado = ChoiceField(
        choices=ESTADOS,
        widget=Select(),
        required=False,
    )
############################################################## DISPONIBILIDADE ###########################################################

def get_dias():
    try:
        today= datetime.now(timezone.utc) 
        diaaberto=Diaaberto.objects.get(datadiaabertoinicio__gte=today,datadiaabertofim__gte=today)
        diainicio= diaaberto.datadiaabertoinicio.date()
        diafim= diaaberto.datadiaabertofim.date()
        totaldias= diafim-diainicio+timedelta(days=1)
        return [('','Escolha o dia')]+[(diainicio+timedelta(days=d),diainicio+timedelta(days=d))for d in range(totaldias.days)]
    except:
        return [('','Escolha o dia')]


TAREFAS_CHOICES = [
    ("tarefaAuxiliar", "Auxiliar em atividades"),
    ("tarefaAcompanhar", "Acompanhar participantes"),
    ("tarefaOutra", "Outras tarefas"),
]

class PreferenciaTarefasForm(forms.Form):
    tipo_tarefa = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=TAREFAS_CHOICES,
    )


class CustomTimeWidget(TimeInput):

    def __init__(self, attrs=None, format=None, input_type=None, default=None):
        input_type = 'time'
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            if default is not None:
                self.attrs = {'class': 'input', 'value': default}
        if format is not None:
            self.format = format
        else: 
            self.format = '%H:%M'

def get_atividades_choices(fac):
    return [("",'Escolha a Atividade')]+[(atividade.id,atividade.nome) for atividade in Atividade.tarefas_get_atividades(fac)]    