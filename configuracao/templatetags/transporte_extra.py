from django import template
from django.core.exceptions import ObjectDoesNotExist
from configuracao.forms import *
from configuracao.models import *

register = template.Library()

@register.filter
def transport_type(value):
    tipo = 'Transporte Universitario'
    try:
        trans = value.transporte#.transportepessoal
        #tipo = trans.tipo
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

@register.filter
def vagas_cap(value):
    vagas = "Não disponivel"
    cap = "Não disponivel"
    try:
        vagas = value.transporte.transporteuniversitario.vagas
        cap = value.transporte.transporteuniversitario.capacidade
        if value == 0:
            vagas = "Sem vagas"
    except ObjectDoesNotExist:
        pass
    return str(vagas) + '/' + str(cap)
