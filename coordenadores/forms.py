from django.forms import * 
from .models import Tarefa,Departamento
from atividades.models import Atividade,Sessao
from colaboradores.models import Colaborador
from datetime import datetime

def get_choices_time():
    return [(str(t),t) for t in range(5, 61, 5)]  

class TarefaForm(ModelForm):
    ativ=[('','------------')]+[(atividade.id,atividade.nome) for atividade in Atividade.objects.filter(nrcolaboradoresnecessario__gt=0)]
    atividades= ChoiceField(choices=ativ)
    sessoes=ChoiceField(choices=[('','------------')])
    dias=ChoiceField(choices=[('','------------')])
    colaborador=ChoiceField(choices=[('','------------')])
    def __init__(self, *args, **kwargs):
        super(TarefaForm, self).__init__(*args, **kwargs)
        self.fields['descricao'].required = False
    class Meta:  
        model = Tarefa 
        exclude = ['coordenadorutilizadorid','id','colaboradorutilizadorid']
        widgets = {
            'tipo': RadioSelect(attrs={'class':'radio'},choices=[('Atividade','Auxiliar Atividade'),('Acompanhar','Acompanhar participantes'),('Outra','Outra')]),
            'atividades' : Select(),
            'descricao': Textarea(attrs={'class':'textarea','maxlength':'100'}), 
            'sessoes' : Select(),
            'dias' : Select(),
            'colaborador' : Select()
            }
        
    

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
