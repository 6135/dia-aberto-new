from django.forms import *
from .models import *
from datetime import datetime
    
class DateTimeWidget(DateTimeInput):

    def __init__(self, attrs=None, format=None, input_type=None):
        now = datetime.now()
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'input datetimepicker', 'value': str(now.date()) + ' ' + str(now.time().strftime('%H:%M'))}
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
            'datadiaabertofim': DateTimeWidget(),
            'datapropostasatividadesincio': DateTimeWidget(),
            'dataporpostaatividadesfim': DateTimeWidget(),
            'datainscricaoatividadesinicio': DateTimeWidget(),
            'datainscricaoatividadesfim': DateTimeWidget(),
        }
    