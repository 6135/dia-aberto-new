from django.forms import ModelForm,CheckboxInput
from .models import Atividade, Sessao, Horario, Espaco, Materiais  

class CheckBoxInputCustom(CheckboxInput):
    input_type = 'checkbox'
    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()

class AtividadeForm(ModelForm):  
    class Meta:  
        model = Atividade  
        exclude = ['coordenadorutilizadorid', 'professoruniversitarioutilizadorid','datasubmissao', 'dataalteracao','estado','id','diaabertoid']

class SessaoForm(ModelForm):  
    class Meta:  
        model = Sessao  
        exclude = ["espacoid", "horarioid", "ninscritos", "vagas"]

class MateriaisForm(ModelForm):  
    class Meta:  
        model = Materiais  
        exclude = ["atividadeid"]
