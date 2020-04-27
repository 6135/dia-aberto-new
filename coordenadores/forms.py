from django.forms import * 
from .models import *
from atividades.models import Atividade,Sessao
from colaboradores.models import Colaborador
from datetime import datetime

class TarefaForm(ModelForm):
    def clean(self):
        cleaned_data=super().clean()
        self.instance.coord = Coordenador.objects.get(utilizador__id=5)
        estado = 'naoConcluida'
        if cleaned_data.get('colab') is None:
            estado = 'naoAtribuida'
        self.instance.estado = estado
        nome = 'Auxiliar atividade'
        if cleaned_data.get('tipo') == 'a':
            self.instance.nome = nome + 'otherstuff'
        elif True:
            print('')

    class Meta:  
        model = Tarefa 
        exclude = ['coord','id','nome','created_at','estado','created_at']
        widgets = {
            'tipo': RadioSelect(attrs={'class':'radio'},choices=[('tarefaAuxiliar','Auxiliar Atividade'),('tarefaAcompanhar','Acompanhar participantes'),('tarefaOutra','Outra')]),
            }
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colab'].queryset = Colaborador.objects.filter().order_by('utilizadorid__nome')

        if 'sessoes' in self.data:
            try:
                sessoes_id = int(self.data.get('sessoes'))
                self.fields['colab'].queryset = Colaborador.objects.filter().order_by('utilizadorid__nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['colab'].queryset = self.instance.colab.none()

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
        ("tarefaAcompanhar", "Acompanhar"),
        ("tarefaAuxiliar", "Auxiliar"),
        ("tarefaOutra", "Outra")
     ],widget=Select())
