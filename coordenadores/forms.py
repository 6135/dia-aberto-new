from django.forms import * 
from .models import *
from atividades.models import Atividade,Sessao
from colaboradores.models import Colaborador
from configuracao.models import Diaaberto
from datetime import datetime,timezone

def get_dias():
    today= datetime.now(timezone.utc) 
    diaaberto=Diaaberto.objects.get(datadiaabertoinicio__lte=today,datadiaabertofim__gte=today)
    diainicio= diaaberto.datadiaabertoinicio.date()
    diafim= diaaberto.datadiaabertofim.date()
    totaldias= diafim-diainicio+timedelta(days=1)
    return [(diainicio+timedelta(days=d),diainicio+timedelta(days=d))for d in range(totaldias.days)]

class TarefaForm(ModelForm):
    def clean(self):
        cleaned_data=super().clean()
        self.instance.coord = Coordenador.objects.get(utilizador__id=5)
        estado = 'naoConcluida'
        if cleaned_data.get('colab') is None:
            estado = 'naoAtribuida'
        self.instance.estado = estado
        nome = Atividade.objects.get(id=self.data.get('atividades')).nome
        if cleaned_data.get('tipo') == 'tarefaAuxiliar':
            self.instance.nome = 'Auxiliar na atividade '+nome
        elif cleaned_data.get('tipo') == 'tarefaAcompanhar':
            nome = 'grupo'
            self.instance.nome = 'Acompanhar o grupo '+nome

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
    ativ=[('','Escolha a Atividade')]+[(atividade.id,atividade.nome) for atividade in Atividade.objects.filter(nrcolaboradoresnecessario__gt=0)]
    atividades= ChoiceField(choices=ativ,widget=Select(attrs={'onchange':'diasSelect();'}))
    sessoes=ChoiceField(choices=[('','Escolha a Sessão')],widget=Select(attrs={'onchange':'colaboradoresSelect();'}))
    dias=ChoiceField(choices=[('','Escolha o Dia')],widget=Select(attrs={'onchange':'sessoesSelect();'}))
    class Meta:
        model= TarefaAuxiliar
        exclude = ['tarefaid']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sessoes'].queryset = Sessao.objects.none()
        print(self.data.get('sessoes'))
        if 'dias' in self.data:
            try:
                dia = self.data.get('dias')
                self.fields['sessoes'].queryset = Sessao.objects.filter(dia=dia)
                print(self.data.get('sessoes'))
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sessoes'].queryset = self.instance.sessoes.none() 
            

class TarefaAcompanharForm(ModelForm):
    class Meta:
        model= TarefaAcompanhar
        exclude = ['tarefaid']
        widgets = {

            }

class TarefaOutraForm(ModelForm):
    dia = ChoiceField(choices=get_dias(),widget=Select())
    horario = DateField(widget=DateInput(attrs={'class':'timepicker'}))
    class Meta:
        model= TarefaOutra
        exclude = ['tarefaid']
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
