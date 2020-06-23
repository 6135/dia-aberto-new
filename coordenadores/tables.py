import django_tables2 as tables
from coordenadores.models import *
from django.utils.html import format_html
from django.db.models import Count
from atividades.models import Tema

class TarefaTable(tables.Table):
    class Meta:
        model = Tarefa
    
    def render_acoes(self,record):
        return  format_html(f"""
            
        """)