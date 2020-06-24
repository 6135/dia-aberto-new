import django_filters
from django.db.models import Exists, OuterRef
import datetime
from coordenadores.models import Tarefa
from configuracao.models import *

from django.forms.widgets import TextInput, CheckboxSelectMultiple

def get_sub_tarefa(queryset, name, value):
       if value[0] == 'tarefaAuxliar':
           return queryset.filter(
            Exists(AuxiliarTarefa.objects.filter(
                tarefaid=OuterRef('pk')
            ))
        )   

class TarefaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name="nome", lookup_expr='icontains')
    estado = django_filters.MultipleChoiceFilter(field_name='estado', choices=[('naoAtribuida','Não Atribuida'),('Concluida','Concluída'),
        ('Cancelada','Cancelada'),('Inicida','Iniciada'),('naoConcluida','Não Concluída')], widget=CheckboxSelectMultiple())
    tipo = django_filters.MultipleChoiceFilter(field_name='tipo', choices=[('tarefaAuxiliar','Auxiliar'),('tarefaAcompanhar','Acompanhar'),
        ('tarefaOutra','Outra')], widget=CheckboxSelectMultiple(),method=get_sub_tarefa)
    dia = django_filters.DateFilter(label="Dia")
    colab = django_filters.NumberFilter(label="colab",field_name="colab__utilizador_ptr_id")
    class Meta:
        model = Tarefa
        fields = '__all__'

