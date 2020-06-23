import django_filters
from utilizadores.models import Utilizador


class UtilizadoresFilter(django_filters.FilterSet):

    class Meta:
        model = Utilizador
        fields = '__all__'
