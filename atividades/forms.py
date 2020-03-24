from django.forms import * 
from .models import Atividade, Sessao,Materiais

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
        exclude = ["vagas","ninscritos"]
        widgets = {
            'participantesmaximo': NumberInput(attrs={'class': 'input'}),
            'espacoid':Select(), 
            'horarioid':Select(),
        }

class MateriaisForm(ModelForm):  
    class Meta:  
        model = Materiais  
        exclude = ["atividadeid"]
