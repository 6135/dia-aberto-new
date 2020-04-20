from django.forms import * 
from .models import Tarefa,Departamento
from datetime import datetime

def get_choices_time():
    return [(str(t),t) for t in range(5, 61, 5)]  

class DateTimeWidget(DateTimeInput):
    
    def __init__(self, attrs=None, format=None, input_type=None, default=None):
        #input_type = 'datetime-local'
        now = datetime.now()
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            if default is not None:
                self.attrs = {'class': 'input', 'value': default}
            else:
                self.attrs = {'class': 'input', 'value': str(now.date()) + ' ' + str(now.time().strftime('%H:%M'))}
        if format is not None:
            self.format = format
        else: 
            self.format = '%Y-%m-%d'


class TarefaForm(ModelForm):
    tipo=[('Atividade','Atividade'),('Acompanhar','Acompanhar participantes')]
    class Meta:  
        model = Tarefa 
        exclude = ['coordenadorutilizadorid','id','colaboradorutilizadorid']
        widgets = {
            'tipo': RadioSelect(),
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
