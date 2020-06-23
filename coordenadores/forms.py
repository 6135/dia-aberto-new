from django.forms import * 
from .models import *
from atividades.models import Atividade,Sessao
from utilizadores.models import Colaborador,Coordenador
from configuracao.models import Departamento, Diaaberto, Horario
from datetime import datetime,timezone,timedelta
from inscricoes.models import Inscricao,Inscricaosessao

def get_dias():
    try:
        today= datetime.now(timezone.utc) 
        diaaberto=Diaaberto.objects.get(datadiaabertoinicio__gte=today,datadiaabertofim__gte=today)
        diainicio= diaaberto.datadiaabertoinicio.date()
        diafim= diaaberto.datadiaabertofim.date()
        totaldias= diafim-diainicio+timedelta(days=1)
        return [('','Escolha o dia')]+[(diainicio+timedelta(days=d),diainicio+timedelta(days=d))for d in range(totaldias.days)]
    except:
        return [('','Escolha o dia')]

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

class TarefaAuxiliarForm(Form):
    atividade = ChoiceField(widget=Select(),choices=[('','Escolha a Atividade')])
    dia = ChoiceField(widget=Select(),choices=[('','Escolha a dia')])
    sessao = ChoiceField(widget=Select(),choices=[('','Escolha o horário')])
    colab = ChoiceField(widget=Select(),choices = [('','Escolha o colaborador')])
    def save():
        pass

class TarefaAcompanharForm(Form):
   
    def save():
        pass

class TarefaOutraForm(Form):
   
    def save():
        pass










#class TarefaForm(ModelForm):
#    horarioTime = TimeField(widget=TimeInput(attrs={'class':'timepicker','type':'time','min':'09:00','max':'18:00'}),required=False)
#    horarioSelect = ChoiceField(widget=Select(),choices=[('','Escolha o horario')],required=False)
#    dias = ChoiceField(widget=Select(),choices = get_dias(),required=False)
#    diasDependentes = ChoiceField(widget=Select(),choices = [('','Escolha o horario')],required=False)
#
#    def clean(self):
#        cleaned_data=super().clean()
#        if cleaned_data.get('tipo') == 'tarefaOutra':
#            self.instance.horario = cleaned_data.get('horarioTime')
#            self.instance.dia = cleaned_data.get('dias')
#        else:
#            if cleaned_data.get('tipo') == 'tarefaAuxiliar':
#                sessao = Sessao.objects.get(id=self.data['sessao'])
#                self.instance.horario = sessao.horarioid.inicio
#            else:   
#                self.instance.horario = cleaned_data.get('horarioSelect')
#            self.instance.dia = cleaned_data.get('diasDependentes')
#
#        estado = 'naoConcluida'
#        if cleaned_data.get('colab') is None:
#            estado = 'naoAtribuida'
#        self.instance.estado = estado
#        if self.data.get('atividades'):
#            nome = Atividade.objects.get(id=self.data.get('atividades')).nome
#        if cleaned_data.get('tipo') == 'tarefaAuxiliar':
#            self.instance.nome = 'Auxiliar na atividade '+nome
#        if cleaned_data.get('tipo') == 'tarefaAcompanhar':
#            nome = self.data.get('inscricao')
#            self.instance.nome = 'Acompanhar o Grupo '+nome
#        elif cleaned_data.get('tipo') == 'tarefaOutra':
#            nome = self.data.get('descricao')
#            self.instance.nome = nome[0:18] + '...'
#            
#    class Meta:  
#        model = Tarefa 
#        exclude = ['coord','id','nome','created_at','estado','horario','dia']
#        widgets = {
#            'tipo': RadioSelect(attrs={'class':'radio'},choices=[('tarefaAuxiliar','Auxiliar Atividade'),('tarefaAcompanhar','Acompanhar participantes'),('tarefaOutra','Outra')]),
#            }
#
#    def __init__(self,user,*args, **kwargs):
#        super().__init__(*args, **kwargs)
#        coordenador = Coordenador.objects.get(user_ptr_id=user)
#        self.fields['colab'].queryset =  Colaborador.objects.filter(faculdade = coordenador.faculdade,utilizador_ptr_id__valido=True).order_by('utilizador_ptr_id__user_ptr_id__first_name')
#        self.instance.coord = Coordenador.objects.get(utilizador_ptr_id__user_ptr_id=user)
#        if 'atividades' in self.data:
#            try:
#                sessoes = Sessao.objects.filter(atividadeid=self.data['atividades'])
#                self.fields['colab'].queryset = Colaborador.objects.filter().order_by('utilizador_ptr_id__user_ptr_id__first_name')
#            except (ValueError, TypeError):
#                pass  
#        elif self.instance.pk:
#            self.fields['colab'].queryset = Colaborador.objects.none()
#
#def get_atividades_choices():
#    return [(" ",'Escolha a Atividade')]+[(atividade.id,atividade.nome) for atividade in Atividade.objects.filter(nrcolaboradoresnecessario__gt=0,estado='Aceite')]
#
#class TarefaAuxiliarForm(ModelForm):
#    atividades= ChoiceField(choices=get_atividades_choices,widget=Select(attrs={'onchange':'diasSelect();'}))
#
#    def __init__(self,*args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['sessao'].queryset =  Sessao.objects.none()
#        if 'diasDependentes' in self.data:
#            try:
#                dia = self.data.get('diasDependentes')
#                atividade = self.data.get('atividades')
#                self.fields['sessao'].queryset = Sessao.objects.filter(dia=dia,atividadeid=atividade)
#            except (ValueError, TypeError):
#                pass  
#        elif self.instance.pk:
#            self.fields['sessao'].queryset = Sessao.objects.none()
#            
#    class Meta:
#        model= TarefaAuxiliar
#        exclude = ['tarefaid']
#        widgets = {   
#            'sessao' : Select(choices=[('','Escolha o horario')])      
#        } 
#            
#def get_inscricao_choices():
#    return [('','Escolha um grupo')]+[(grupo.id,'Grupo '+str(grupo.id)) for grupo in Inscricao.objects.filter(nalunos__gt=1)]
#
#class TarefaAcompanharForm(ModelForm):
#    inscricao =  ChoiceField(choices=get_inscricao_choices,widget=Select(attrs={'onchange':'grupoInfo();diasGrupo();'}))
#    class Meta:
#        model= TarefaAcompanhar
#        exclude = ['tarefaid','inscricao','dias']
#        widgets ={
#            'origem' : Select(choices=[('','Escolha o local de encontro')],attrs={'onchange':'grupoDestino();'}),
#            'destino' : Select(choices=[('','Escolha o local de destino')],)
#        }
#
#    def clean(self):
#        cleaned_data=super().clean()
#        self.instance.inscricao = Inscricao.objects.get(id=cleaned_data['inscricao']) 
#        
#def get_dia_choices():
#    return [('','Escolha o dia')]+get_dias()
#
#class TarefaOutraForm(ModelForm):
#    class Meta:
#        model= TarefaOutra
#        exclude = ['tarefaid']
#        widgets = {
#            'descricao' : Textarea(attrs={'class':'textarea'}),
#            }           
#   
#def get_dep_choices():
#    return [(-1,'Mostra todos os Departamentos')] + [(departamento.id,departamento.nome) for departamento in Departamento.objects.all()]
#
class tarefaFilterForm(Form):
    searchTarefa = CharField(widget=TextInput(attrs={'class': 'input','placeholder':'Pesquisa'}), required=False)
    Concluida=BooleanField(widget=CheckboxInput(),required=False)
    naoConcluida=BooleanField(widget=CheckboxInput(),required=False)
    naoAtribuida=BooleanField(widget=CheckboxInput(),required=False)
    departamentos = ChoiceField(choices=get_dep_choices,widget=Select(), required=False)
    tipo = ChoiceField(choices=[
        (" ", "Mostrar todos os tipos de Tarefa"),
        ("tarefaAcompanhar", "Acompanhar"),
        ("tarefaAuxiliar", "Auxiliar"),
        ("tarefaOutra", "Outra")
     ],widget=Select())
