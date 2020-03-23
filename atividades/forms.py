from django.forms import ModelForm,CheckboxInput
from .models import Atividade, Sessao, Horario, Espaco  

class CheckBoxInputCustom(CheckboxInput):
    input_type = 'checkbox'
    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()

class AtividadeForm(ModelForm):  
    class Meta:  
        model = Atividade  
        exclude = ['coordenadorutilizadorid', 'professoruniversitarioutilizadorid','datasubmissao', 'dataalteracao','estado','id','diabertoid']

class SessaoForm(ModelForm):  
    class Meta:  
        model = Sessao  
        exclude = ["espacoid", "horarioid", "ninscritos", "vagas"]

class HorarioForm(ModelForm):  
    class Meta:  
        model = Horario
        fields = '__all__'

class EspacoForm(ModelForm):  
    class Meta:  
        model = Espaco
        fields = '__all__'

