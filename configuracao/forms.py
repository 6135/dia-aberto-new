from django.forms import *
from .models import *
from datetime import datetime
    
class DateTimeWidget(DateTimeInput):

    def __init__(self, attrs=None, format=None, input_type=None, hours='09', minutes='00', default=None):
        #input_type = 'datetime-local'
        now = datetime.now()
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            if default is not None:
                self.attrs = {'class': 'input', 'value': default}
            if hours and minutes is not None:
                self.attrs = {'class': 'input', 'value': str(now.date()) + ' ' + hours + ':' + minutes}
            else:
                self.attrs = {'class': 'input', 'value': str(now.date()) + ' ' + str(now.time().strftime('%H:%M'))}
        if format is not None:
            self.format = format
        else: 
            self.format = '%Y-%m-%d %H:%M'

class diaAbertoSettingsForm(ModelForm):  
    #descricao = CharField(widget=TinyMCE())
    class Meta:
        now = datetime.now()
        model = Diaaberto
        exclude = ['administradorutilizadorid', 'id']
        widgets = {
            'enderecopaginaweb': TextInput(attrs={'class': 'input'}),
            'emaildiaaberto': EmailInput(attrs={'class': 'input'}),
            'ano': NumberInput(attrs={'class': 'input', 'value': now.year}),
            'datadiaabertoinicio': DateTimeWidget(),
            'datadiaabertofim': DateTimeWidget(hours='17', minutes='00'),
            'datapropostasatividadesincio': DateTimeWidget(hours='23', minutes='55'),
            'dataporpostaatividadesfim': DateTimeWidget(hours='23', minutes='55'),
            'datainscricaoatividadesinicio': DateTimeWidget(hours='23', minutes='55'),
            'datainscricaoatividadesfim': DateTimeWidget(hours='23', minutes='55'),
            'descricao': Textarea(attrs={'class':'textarea'})
        }
    
class diaAbertoFilterForm(Form):
    searchAno = CharField(widget=NumberInput, required=False)
    orderByChoices = [('', 'Nao ordenar'),
        ('ano', 'Ordernar por: Ano'),
        ('-ano', 'Ordernar por: Ano (Decrescente)'),
        ('datadiaabertoinicio', 'Ordernar por: Inicio'),
        ('-datadiaabertoinicio', 'Ordernar por: Inicio (Descrescente)'),
        ('datadiaabertofim', 'Ordernar por: Fim'),
        ('-datadiaabertofim', 'Ordernar por: Fim (Descrescente)'),
    ]
    orderBy = ChoiceField(choices=orderByChoices, widget=Select(), required=False)

    showByChoices = [('','Mostrar todos'),
        ('1','Mostrar: Dias Abertos Ativos'),
        ('2','Mostrar: Submissao de Atividades Ativas'),
        ('3','Mostrar: Submissao de Inscricoes Ativas'),
    ]
    showBy = ChoiceField(choices=showByChoices, widget=Select(), required=False)

class menuForm(ModelForm):
    diaaberto = ChoiceField(choices=[(dia.id,dia.ano) for dia in Diaaberto.objects.all()],widget=Select(), required=True)
    campus = ChoiceField(choices=[(camp.id,camp.nome) for camp in Campus.objects.all()],widget=Select(), required=True)
    tipo = ChoiceField(choices=[
            ('Carne',"Carne"),
            ('Peixe','Peixe'),
            ('Vegetariano', 'Vegetariano'),
        ],widget=Select())
    class Meta:
        model = Menu
        exclude = ['id','horarioid','campus','diaaberto']
        widgets={
            'precoalunos': NumberInput(attrs={'class':'input', 'step': '0.01','min': '0'}),
            'precoprofessores': NumberInput(attrs={'class':'input','step': '0.01','min': '0'})
        }

class pratosForm(ModelForm):
    class Meta:
        model = Prato
        exclude = ['id','menuid']
        widgets = {
            'prato': TextInput(attrs={'class':'input'}),
            'nrpratosdisponiveis': NumberInput(attrs={'class':'input'}),
        }