from django.forms import ModelForm
from .models import Inscricaoindividual


class InscricaoIndividualForm(ModelForm):
    class Meta:
        model = Inscricaoindividual
        exclude = ('participante',)
