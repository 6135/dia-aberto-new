from django.forms import ModelForm,CheckboxInput
from .models import Atividade, Sessao, Horario, Espaco, Materiais  
from django.forms.widgets import NumberInput, Select, TextInput, Textarea

class CheckBoxInputCustom(CheckboxInput):
    input_type = 'checkbox'
    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()

class AtividadeForm(ModelForm):  
    class Meta:  
        model = Atividade  
        exclude = ['coordenadorutilizadorid', 'professoruniversitarioutilizadorid','datasubmissao', 'dataalteracao','estado','id','diaabertoid']
        widgets = {
            'nome': TextInput(attrs={'class': 'input'}),
            'tipo': Select(),
            'descricao': Textarea(attrs={'class':'textarea'}),
            'publicoalvo': Select(),
            'nrcolaboradoresnecessario': NumberInput(attrs={'class': 'input'}),
            'duracaoesperada': NumberInput(attrs={'class': 'input'}),
            'participantesmaximo': NumberInput(attrs={'class': 'input'}),
            }

class SessaoForm(ModelForm):  
    class Meta:  
        model = Sessao  
        exclude = ["espacoid", "horarioid", "ninscritos", "vagas"]
        widgets = {
            'participantesmaximo': NumberInput(attrs={'class': 'input'}),
            'duracaomedia': NumberInput(attrs={'class': 'input'}),
            }

class MateriaisForm(ModelForm):
    class Meta:  
        model = Materiais  
        exclude = ["atividadeid"]
        widgets = {
            'nomematerial': TextInput(attrs={'class': 'input'}),
            }

