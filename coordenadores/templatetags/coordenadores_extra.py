from django import template
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()
from configuracao.models import Espaco
@register.filter
def colab_none(colab):
    if colab is None or str(colab) == 'None':
        return 'N/A'
    else:
        return colab.full_name

@register.filter
def local(id):
    if id != 'Check in':
        espaco = Espaco.objects.get(id=int(id))
        return "Sala "+str(espaco)+", Edifício " + espaco.edificio.__str__()
    else:
        return 'Check in'
        