
import django_filters
from coordenadores.models import Tarefa, TarefaAcompanhar, TarefaAuxiliar, TarefaOutra
from django.db.models import Exists, OuterRef


def filter_tipo(queryset, name, value):
    if value == 'tarefaAcompanhar':
        return queryset.filter(Exists(TarefaAcompanhar.objects.filter(tarefaid=OuterRef('id'))))
    elif value == 'tarefaAuxiliar':
        return queryset.filter(Exists(TarefaAuxiliar.objects.filter(tarefaid=OuterRef('id'))))
    elif value == 'tarefaOutra':
        return queryset.filter(Exists(TarefaOutra.objects.filter(tarefaid=OuterRef('id'))))
    return queryset


class TarefasFilter(django_filters.FilterSet):

    tipo = django_filters.CharFilter(method=filter_tipo)

    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')

    class Meta:
        model = Tarefa
        fields = '__all__'
