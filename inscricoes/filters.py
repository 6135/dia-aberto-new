import django_filters
from .models import *

class InscricaoFilter(django_filters.FilterSet):
    class Meta:
        model = Inscricao
