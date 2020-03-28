from django.forms import * 
from .models import Atividade, Sessao,Materiais,Horario,Espaco

class AtividadeForm(ModelForm):
    espacoid = ChoiceField(choices=[(espaco.id, espaco.nome+' '+espaco.edificio) for espaco in Espaco.objects.all()])
    class Meta:  
        model = Atividade  
        exclude = ['coordenadorutilizadorid', 'professoruniversitarioutilizadorid','datasubmissao', 'dataalteracao','estado','id','diaabertoid']
        widgets = {
            'nome': TextInput(attrs={'class': 'input'}),
            'tipo': Select(),
            'descricao': Textarea(attrs={'class':'textarea'}),
            'publicoalvo': Select(),
            'nrcolaboradoresnecessario': NumberInput(attrs={'class': 'input','min':0}),
            'participantesmaximo': NumberInput(attrs={'class': 'input','min':1}),
            'espacoid':Select(), 
        }

class SessaoForm(ModelForm):  
    horarioid = ChoiceField(choices=[(horario.id, str(horario.inicio.strftime('%H:%M')) + '  até  ' + str(horario.fim.strftime('%H:%M'))) for horario in Horario.objects.all()])
    class Meta:  
        model = Sessao  
        exclude = ['id',"vagas","ninscritos"]
        widgets = {
            'horarioid':Select(),
        }

class MateriaisForm(ModelForm):  
    class Meta:  
        model = Materiais  
        exclude = ["atividadeid"]
