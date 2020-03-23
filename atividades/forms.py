from django.forms import ModelForm,CheckboxInput, Form
from .models import Atividade, Sessao, Horario, Espaco  
from django.forms.fields import DateField, TypedChoiceField




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

class HorarioSessaoForm(Form):
    inicio= ChoiceField(choices=Horario.objects.only("inicio"), required=True)  
    fim= Field(choices=Horario.objects.only("fim"), required=True)

class EspacoForm(ModelForm):  
    class Meta:  
        model = Espaco
        fields = '__all__'

