from django.forms import ModelForm,CheckboxInput
from .models import Atividade, Sessao, Horario, Materiais  
from django.forms.widgets import NumberInput, Select, TextInput, Textarea



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
        }

class SessaoForm(ModelForm):  
    class Meta:  
        model = Sessao
        exclude = ["espacoid", "horarioid", "ninscritos", "vagas"]

class MateriaisForm(ModelForm):  
    class Meta:  
        model = Materiais  
        exclude = ["atividadeid"]
