import django_tables2 as tables
from .models import Inscricao, Escola
import itertools
from django_tables2.utils import Accessor

class InscricoesTable(tables.Table):
    ninscricao = tables.Column(accessor='ninscricao')

    class Meta:
        model = Inscricao
   
class EscolaTable(tables.Table):

    class Meta:
        model = Escola   
 

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.counter = itertools.count()

    # def render_ano(self, value, record):
    #     return format_html("<b>{} {}</b>", value, record.ano)

    # def render_turma(self):
    #     return "Row %d" % next(self.counter)