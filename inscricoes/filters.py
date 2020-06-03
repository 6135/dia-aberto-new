import django_filters
from .models import *


class InscricaoFilter(django_filters.FilterSet):
    areacientifica = django_filters.CharFilter(
        field_name="areacientifica", lookup_expr='istartswith')

    class Meta:
        model = Inscricao
        fields = '__all__'
