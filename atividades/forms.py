from django.forms import ModelForm,CheckboxInput
from .models import Atividade, Sessao, Horario, Espaco, Materiais
from django.forms.widgets import NumberInput, Select, TextInput, Textarea
from django.forms.fields import ChoiceField

class CheckBoxInputCustom(CheckboxInput):
    input_type = 'checkbox'
    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()


def get_choices_time():
    return [(str(t),t) for t in range(5, 61, 5)]


class AtividadeForm(ModelForm):
    duracaoesperada= ChoiceField(choices=get_choices_time())  
    class Meta:  
        model = Atividade  
        exclude = ['coordenadorutilizadorid', 'professoruniversitarioutilizadorid','datasubmissao', 'dataalteracao','estado','id','diaabertoid', "espacoid","tema"]
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


class MateriaisForm(ModelForm):
    class Meta:  
        model = Materiais  
        exclude = ["atividadeid"]
        widgets = {
            'nomematerial': TextInput(attrs={'class': 'input'}),
            }
