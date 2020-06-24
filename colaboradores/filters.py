
import django_filters
from coordenadores.models import Tarefa


class TarefasFilter(django_filters.FilterSet):

    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')

    class Meta:
        model = Tarefa
        fields = '__all__'
