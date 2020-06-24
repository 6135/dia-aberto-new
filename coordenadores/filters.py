import django_filters
from django.db.models import Exists, OuterRef
import datetime
from coordenadores.models import Tarefa
from configuracao.models import *

from django.forms.widgets import TextInput

class TarefaFilter(django_filters.FilterSet):

    class Meta:
        model = Tarefa
        fields = '__all__'

