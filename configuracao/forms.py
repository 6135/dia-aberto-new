from django.forms import *
from .models import *
from datetime import datetime
    
class DateTimeWidget(DateTimeInput):

    def __init__(self, attrs=None, format=None, input_type=None, hours='09', minutes='00'):
        #input_type = 'datetime-local'
        now = datetime.now()
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
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
            'descricao': Textarea(attrs={'class': 'textare'}),
            'datadiaabertoinicio': DateTimeWidget(),
            'datadiaabertofim': DateTimeWidget(hours='17', minutes='00'),
            'datapropostasatividadesincio': DateTimeWidget(hours=None, minutes=None),
            'dataporpostaatividadesfim': DateTimeWidget(hours=None, minutes=None),
            'datainscricaoatividadesinicio': DateTimeWidget(hours=None, minutes=None),
            'datainscricaoatividadesfim': DateTimeWidget(hours=None, minutes=None),
        }
    