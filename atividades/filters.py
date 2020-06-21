from atividades.models import Atividade
import django_filters


class AtividadeFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    campus_id = django_filters.NumberFilter(
        field_name="espacoid__edificio__campus__id")
    unidade_organica_id = django_filters.NumberFilter(
        field_name="espacoid__edificio__campus__id")
    # TODO: Adicionar filtros
    # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Atividade
        fields = '__all__'
