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


