from django.forms import * 
from configuracao.models import Departamento

class tarefaFilterForm(Form):
    searchTarefa = CharField(widget=TextInput(attrs={'class': 'input','placeholder':'Tarefa'}), required=False)
    Concluida=BooleanField(widget=CheckboxInput(),required=False)
    naoConcluida=BooleanField(widget=CheckboxInput(),required=False)
    dep=[(-1,'Mostra todos os Departamentos')] + [(departamento.id,departamento.nome) for departamento in Departamento.objects.all()]
    departamentos = ChoiceField(choices=dep,widget=Select(), required=False)
    tipo = ChoiceField(choices=[
        (" ", "Mostrar todos os tipos de Tarefa"),
        ("Percurso", "Percurso"),
        ("Atividade", "Atividade"),
        ("Outra", "Outra")
     ],widget=Select())