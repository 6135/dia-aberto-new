from django import forms  
from .models import Atividade, Sessao, Horario, Espaco  

class AtividadeForm(forms.ModelForm):  
    class Meta:  
        model = Atividade  
        exclude = ['coordenadorutilizadorid', 'professoruniversitarioutilizadorid','datasubmissao', 'dataalteracao','estado','id','diaabertoid']

class SessaoForm(forms.ModelForm):  
    class Meta:  
        model = Sessao  
        exclude = ["espacoid", "horarioid","vagas","ninscritos"]

class HorarioForm(forms.ModelForm):  
    class Meta:  
        model = Horario
        exclude = ["id", "participantesmaximo"]  

class EspacoForm(forms.ModelForm):  
    class Meta:  
        model = Espaco
        fields = '__all__'
