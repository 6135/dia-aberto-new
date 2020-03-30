from django.forms import *
from .models import *
from datetime import datetime
from tinymce.widgets import TinyMCE
    
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

    class Meta:
        now = datetime.now()
        model = Diaaberto
        exclude = ['administradorutilizadorid', 'id']
        widgets = {
            'enderecopaginaweb': TextInput(attrs={'class': 'input'}),
            'emaildiaaberto': EmailInput(attrs={'class': 'input'}),
            'ano': NumberInput(attrs={'class': 'input', 'value': now.year}),
            'descricao': TinyMCE(attrs={'class': 'textarea','rows': '5'}),
            'datadiaabertoinicio': DateTimeWidget(),
            'datadiaabertofim': DateTimeWidget(hours='17', minutes='00'),
            'datapropostasatividadesincio': DateTimeWidget(hours=None, minutes=None),
            'dataporpostaatividadesfim': DateTimeWidget(hours=None, minutes=None),
            'datainscricaoatividadesinicio': DateTimeWidget(hours=None, minutes=None),
            'datainscricaoatividadesfim': DateTimeWidget(hours=None, minutes=None),
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
