from django import template
from django.core.exceptions import ObjectDoesNotExist
from configuracao.forms import *
from configuracao.models import *

register = template.Library()

@register.filter
def transport_type(value):
    tipo = 'Transporte Universitario'
    try:
        trans = value.transporte.transportepessoal
        tipo = trans.tipo
    except ObjectDoesNotExist:
        pass
    return tipo

@register.filter
def transport_id(value):
    id = 'Não aplicável'
    try:
        trans = value.transporte.transporteuniversitario
        id = value.transporte.identificador
    except ObjectDoesNotExist:
        pass
    return id