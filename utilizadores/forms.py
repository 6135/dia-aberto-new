from django.forms import ModelForm
from .models import Participante


class ParticipanteForm(ModelForm):
    class Meta:
        model = Participante
        fields = '__all__'
