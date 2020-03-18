from django.forms import ModelForm
from .models import Inscricaoindividual, Inscricaocoletiva, Escola


class InscricaoIndividualForm(ModelForm):
    class Meta:
        model = Inscricaoindividual
        exclude = ('participante',)

class InscricaoColetivaForm(ModelForm):
    class Meta:
        model = Inscricaocoletiva
        exclude = ('participante','escola',)

class EscolaForm(ModelForm):
    class Meta:
        model = Escola
        fields = '__all__'

