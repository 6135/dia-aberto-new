from django.forms import * 
from .models import *
from atividades.models import Atividade,Sessao
from colaboradores.models import Colaborador
from datetime import datetime

class TarefaForm(ModelForm):
    colaboradorutilizadorid=ChoiceField(choices=[('','------------')],widget=Select())

    def clean(self):
        #print(self.data)
        cleaned_data=super().clean()
        print(cleaned_data)
        colaboradorutilizadorid_data=cleaned_data.get('colaboradorutilizadorid')
        print(colaboradorutilizadorid_data)
        if colaboradorutilizadorid_data:
            cleaned_data['colaboradorutilizadorid']=Colaborador.objects.get(utilizadorid__id=colaboradorutilizadorid_data)
            print(cleaned_data.get('colaboradorutilizadorid'))
        else:
            raise ValidationError('Colaborador não é válido')

    class Meta:  
        model = Tarefa 
        exclude = ['coordenadorutilizadorid','id','nome','created_at','estado','colaboradorutilizadorid']
        widgets = {
            'tipo': RadioSelect(attrs={'class':'radio'},choices=[('tarefaAuxiliar','Auxiliar Atividade'),('tarefaAcompanhar','Acompanhar participantes'),('tarefaOutra','Outra')]),
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
        model= TarefaAcompanhar
        exclude = ['tarefaid']
        widgets = {

            }

class TarefaOutraForm(ModelForm):
    class Meta:
        model= TarefaOutra
        exclude = []
        widgets = {
            'descricao' : Textarea(attrs={'class':'textarea'}),
            }           
    

class tarefaFilterForm(Form):
    searchTarefa = CharField(widget=TextInput(attrs={'class': 'input','placeholder':'Pesquisa'}), required=False)
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
