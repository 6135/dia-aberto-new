from django.forms import * 
from configuracao.models import Departamento

class tarefaFilterForm(Form):
    searchAtividade = CharField(widget=TextInput(attrs={'class': 'input','placeholder':'Atividade'}), required=False)
    Realizada=BooleanField(widget=CheckboxInput(),required=False)
    PorRealizar=BooleanField(widget=CheckboxInput(),required=False)
    dep=[(-1,'Mostra todos os Departamentos')] + [(departamento.id,departamento.nome) for departamento in Departamento.objects.all()]
    departamentos = ChoiceField(choices=dep,widget=Select(), required=False)
    tipo = ChoiceField(choices=[
        (" ", "Mostrar todos os tipos de Tarefa"),
        ("Percurso", "Percurso"),
        ("Atividade", "Atividade"),
        ("Outra", "Outra")
     ],widget=Select())