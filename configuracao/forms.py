from django.forms import ModelForm, DateTimeInput, DateInput
from .models import *

class DateTimeWidget(DateTimeInput):
    input_type = 'datetime-local'
    def __init__(self, attrs=None, format=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'input datetimepicker'}
        if format is not None:
            self.format = format.copy()
        else: 
            self.format = '%Y-%m-%d %H:%M'

class diaAbertoSettingsForm(ModelForm):  
    class Meta:
        model = Diaaberto
        exclude = ['administradorutilizadorid', 'id']
        widgets = {
            'datadiaabertoinicio': DateTimeWidget(),
            'datadiaabertofim': DateTimeWidget(),
            'datapropostasatividadesincio': DateTimeWidget(),
            'dataporpostaatividadesfim': DateTimeWidget(),
            'datainscricaoatividadesinicio': DateTimeWidget(),
            'datainscricaoatividadesfim': DateTimeWidget(),
        }
    