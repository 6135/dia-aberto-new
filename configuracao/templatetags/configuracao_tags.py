from django import template
from django.core.exceptions import ObjectDoesNotExist
from configuracao.forms import *
from configuracao.models import *
from configuracao import views
import json

register = template.Library()

@register.filter
def force_required(value):
    value_str = str(value)
    value_str = value_str[:-1] + ' required>'
    print(value_str)
    return value_str

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
    #vagas = "Não disponivel"
    cap = "Não disponivel"
    try:
        #vagas = value.transporte.transporteuniversitario.vagas
        cap = value.transporte.transporteuniversitario.capacidade
        #if value == 0:
            #vagas = "Sem vagas"
    except ObjectDoesNotExist:
        pass
    return str(cap)#str(vagas) + '/' + str(cap)

@register.filter
def pretty_json(value):
    return json.dumps(value, indent=4)
