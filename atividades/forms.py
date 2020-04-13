from django.forms import * 
from .models import Atividade, Sessao,Materiais,Horario,Espaco,Tema
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


class AtividadeForm(ModelForm):
    tema = ChoiceField(choices=[(tema.id,tema.tema) for tema in Tema.objects.all()])
    duracaoesperada= ChoiceField(choices=get_choices_time())
    class Meta:  
        model = Atividade  
        exclude = ['coordenadorutilizadorid', 'professoruniversitarioutilizadorid','datasubmissao', 'dataalteracao','estado','id','diaabertoid','tema','espacoid']
        widgets = {
            'nome': TextInput(attrs={'class': 'input'}),
            'tipo': Select(),
            'descricao': Textarea(attrs={'class':'textarea'}),
            'publicoalvo': Select(),
            'nrcolaboradoresnecessario': NumberInput(attrs={'class': 'input'}),
            'duracaoesperada': NumberInput(attrs={'class': 'input'}),
            'participantesmaximo': NumberInput(attrs={'class': 'input'}),
            'duracaoesperada': Select(),
            }


class SessaoForm(ModelForm):
    class Meta:
        model = Sessao
        fields = ["dia"]
        

class MateriaisForm(ModelForm):
    class Meta:
        model = Materiais  
        exclude = ["atividadeid"]
        widgets = {
            'nomematerial': TextInput(attrs={'class': 'input'}),
            }

class atividadesFilterForm(Form):
    searchAtividade = CharField(widget=TextInput, required=False)
    #orderByChoices = [('', 'Nao ordenar'),
    #    ('ano', 'Ordernar por: Ano'),
    #    ('-ano', 'Ordernar por: Ano (Decrescente)'),
    #    ('datadiaabertoinicio', 'Ordernar por: Inicio'),
    #    ('-datadiaabertoinicio', 'Ordernar por: Inicio (Descrescente)'),
    #    ('datadiaabertofim', 'Ordernar por: Fim'),
    #    ('-datadiaabertofim', 'Ordernar por: Fim (Descrescente)'),
    #]
    #orderBy = ChoiceField(choices=orderByChoices, widget=Select(), required=False)

    showByChoices = [('','Mostrar todos'),
        ('Aceite','Mostrar: Atividades Aceites'),
        ('Recusada','Mostrar: Atividades Recusadas'),
        ('Pendente','Mostrar: Atividades Pendentes'),
    ]
    showBy = ChoiceField(choices=showByChoices, widget=Select(), required=False)