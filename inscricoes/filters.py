import django_filters
from .models import *
from django.db.models import Exists, OuterRef


def filter_departamento(queryset, name, value):
    return queryset.filter(
        Exists(Inscricaosessao.objects.filter(
            inscricao=OuterRef('pk'),
            sessao__atividadeid__professoruniversitarioutilizadorid__departamento_id=value
        ))
    )


class InscricaoFilter(django_filters.FilterSet):
    areacientifica = django_filters.CharFilter(
        field_name="areacientifica", lookup_expr='icontains')
    min_alunos = django_filters.NumberFilter(
        field_name="nalunos", lookup_expr='gte')
    max_alunos = django_filters.NumberFilter(
        field_name="nalunos", lookup_expr='lte')
    departamento = django_filters.CharFilter(method=filter_departamento)
    participante = django_filters.CharFilter(
        field_name="participante__nome", lookup_expr='icontains')

    class Meta:
        model = Inscricao
        fields = '__all__'
