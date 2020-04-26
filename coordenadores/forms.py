from django.forms import * 
from .models import *
from atividades.models import Atividade,Sessao
from colaboradores.models import Colaborador
from datetime import datetime

def get_choices_time():
    return [(str(t),t) for t in range(5, 61, 5)]  

class TarefaForm(ModelForm):
    colaborador=ChoiceField(choices=[('','------------')])
    class Meta:  
        model = Tarefa 
        exclude = ['coordenadorutilizadorid','id','colaboradorutilizadorid']
        widgets = {
            'tipo': RadioSelect(attrs={'class':'radio'},choices=[('tarefaAuxiliar','Auxiliar Atividade'),('tarefaAcompanhar','Acompanhar participantes'),('tarefaOutra','Outra')]),
            'colaborador' : Select()
            }

class TarefaAuxiliarForm(ModelForm):
    ativ=[('','Escolha')]+[(atividade.id,atividade.nome) for atividade in Atividade.objects.filter(nrcolaboradoresnecessario__gt=0)]
    atividades= ChoiceField(choices=ativ,widget=Select(attrs={'onchange':'diasSelect();'}))
    sessoes=ChoiceField(choices=[('','------------')],widget=Select(attrs={'onchange':'colaboradoresSelect();'}))
    dias=ChoiceField(choices=[('','------------')],widget=Select(attrs={'onchange':'sessoesSelect();'}))

    class Meta:
        model= TarefaAuxiliar
        exclude = ['tarefaid']
        
class TarefaAcompanharForm(ModelForm):

    class Meta:
        model= TarefaAuxiliar
        exclude = ['tarefaid']
        widgets = {

            }

class TarefaOutraForm(ModelForm):
    class Meta:
        model= TarefaAuxiliar
        exclude = ['tarefaid']
        widgets = {
            'descricao' : Textarea(attrs={'class':'textarea'}),
            }           
    

class tarefaFilterForm(Form):
    searchTarefa = CharField(widget=TextInput(attrs={'class': 'input','placeholder':'Tarefa'}), required=False)
    Concluida=BooleanField(widget=CheckboxInput(),required=False)
    naoConcluida=BooleanField(widget=CheckboxInput(),required=False)
    naoAtribuida=BooleanField(widget=CheckboxInput(),required=False)
    dep=[(-1,'Mostra todos os Departamentos')] + [(departamento.id,departamento.nome) for departamento in Departamento.objects.all()]
    departamentos = ChoiceField(choices=dep,widget=Select(), required=False)
    tipo = ChoiceField(choices=[
        (" ", "Mostrar todos os tipos de Tarefa"),
        ("Acompanhar", "Acompanhar"),
        ("Auxiliar", "Auxiliar"),
        ("Outra", "Outra")
     ],widget=Select())
