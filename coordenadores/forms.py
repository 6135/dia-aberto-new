from django.forms import * 
from .models import *
from atividades.models import Atividade,Sessao
from utilizadores.models import Colaborador
from configuracao.models import Departamento, Diaaberto
from datetime import datetime,timezone
from inscricoes.models import Inscricao

def get_dias():
    try:
        today= datetime.now(timezone.utc) 
        diaaberto=Diaaberto.objects.get(datadiaabertoinicio__lte=today,datadiaabertofim__gte=today)
        diainicio= diaaberto.datadiaabertoinicio.date()
        diafim= diaaberto.datadiaabertofim.date()
        totaldias= diafim-diainicio+timedelta(days=1)
        return [(diainicio+timedelta(days=d),diainicio+timedelta(days=d))for d in range(totaldias.days)]
    except:
        return []

class CustomTimeWidget(TimeInput):

    def __init__(self, attrs=None, format=None, input_type=None, default=None):
        input_type = 'time'
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            if default is not None:
                self.attrs = {'class': 'input', 'value': default}
        if format is not None:
            self.format = format
        else: 
            self.format = '%H:%M'

class TarefaForm(ModelForm):
  
    def clean(self):
        cleaned_data=super().clean()
        self.instance.coord = Coordenador.objects.get(utilizador__id=5)
        estado = 'naoConcluida'
        if cleaned_data.get('colab') is None:
            estado = 'naoAtribuida'
        self.instance.estado = estado
        if self.data.get('atividades'):
            nome = Atividade.objects.get(id=self.data.get('atividades')).nome
        if cleaned_data.get('tipo') == 'tarefaAuxiliar':
            self.instance.nome = 'Auxiliar na atividade '+nome
        if cleaned_data.get('tipo') == 'tarefaAcompanhar':
            nome = self.data.get('grupo')
            self.instance.nome = 'Acompanhar o '+nome
        elif cleaned_data.get('tipo') == 'tarefaOutra':
            nome = self.data.get('descricao')
            self.instance.nome = nome[0:18] + '...'
    class Meta:  
        model = Tarefa 
        exclude = ['coord','id','nome','created_at','estado','created_at']
        widgets = {
            'tipo': RadioSelect(attrs={'class':'radio'},choices=[('tarefaAuxiliar','Auxiliar Atividade'),('tarefaAcompanhar','Acompanhar participantes'),('tarefaOutra','Outra')]),
            }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colab'].queryset =  Colaborador.objects.filter().order_by('utilizador_ptr_id__user_ptr_id__first_name')

        if 'sessaoid' in self.data:
            try:
                sessoes_id = int(self.data.get('sessaoid'))
                self.fields['colab'].queryset = Colaborador.objects.filter().order_by('utilizador_ptr_id__user_ptr_id__first_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['colab'].queryset = Colaborador.objects.none()

class TarefaAuxiliarForm(ModelForm):
    ativ=[(" ",'Escolha a Atividade')]+[(atividade.id,atividade.nome) for atividade in Atividade.objects.filter(nrcolaboradoresnecessario__gt=0)]
    atividades= ChoiceField(choices=ativ,widget=Select(attrs={'onchange':'diasSelect();'}))
    dias=DateField(widget=Select(attrs={'onchange':'sessoesSelect();'}))
    class Meta:
        model= TarefaAuxiliar
        exclude = ['tarefaid']
        widgets = {         
            'sessaoid' : Select(attrs={'onchange':'colaboradoresSelect();'})
        }
     

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sessaoid'].queryset =  Sessao.objects.all()
        if 'dias' in self.data:
            try:
                dia = self.data.get('dias')
                self.fields['sessaoid'].queryset = Sessao.objects.filter(dia=dia)
                print(self.fields['sessaoid'].queryset)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sessaoid'].queryset = Sessao.objects.none()
            

class TarefaAcompanharForm(ModelForm):
    grupos = [('','Escolha um grupo')]+[(grupo.id,'Grupo '+str(grupo.id)) for grupo in Inscricao.objects.filter(nalunos__gt=1)]
    grupo =  ChoiceField(choices=grupos,widget=Select(attrs={'onchange':'grupoInfo();diasGrupo();'}))
    dias = DateField(widget=Select(attrs={'onchange':'grupoHorario();'}))
    class Meta:
        model= TarefaAcompanhar
        exclude = ['tarefaid']
        widgets ={
            'horario' : Select(attrs={'onchange':'grupoLocal();'}),
            'origem' : Select(attrs={'onchange':'grupoDestino();'}),
            'destino' : Select()
        }

class TarefaOutraForm(ModelForm):
    dia = ChoiceField(choices=get_dias(),widget=Select())
    #horario = DateField(widget=DateInput(attrs={'class':'timepicker'}))
    class Meta:
        model= TarefaOutra
        exclude = ['tarefaid']
        widgets = {
            'descricao' : Textarea(attrs={'class':'textarea'}),
            'horario' : CustomTimeWidget(attrs={'class':'input'})
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
