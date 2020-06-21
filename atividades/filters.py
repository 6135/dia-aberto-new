from atividades.models import Atividade, Sessao
import django_filters
from django.db.models import Exists, OuterRef


def filter_atividade_que_tem_sessoes_no_dia(queryset, name, value):
    print(value)
    return queryset.filter(
        Exists(Sessao.objects.filter(
            atividadeid=OuterRef('id'),
            dia=value
        ))
    )


class AtividadeFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    campus_id = django_filters.NumberFilter(
        field_name="espacoid__edificio__campus__id")
    departamento_id = django_filters.NumberFilter(
        field_name="professoruniversitarioutilizadorid__departamento__id")
    dia = django_filters.DateFilter(
        method=filter_atividade_que_tem_sessoes_no_dia)
    # TODO: Adicionar filtros
    # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Atividade
        fields = '__all__'
