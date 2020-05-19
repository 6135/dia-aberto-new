from django import template
from django.core.exceptions import ObjectDoesNotExist
from configuracao.forms import *
from configuracao.models import *
from configuracao import views
import json

register = template.Library()

@register.filter
def field_data(value):
    classes = 'class="' + value.field.widget.attrs['class'] + '"'
    result = str(classes)
    if value.name == 'dia':
        result += ' onchange="getSchedules(\'' + str(value.auto_id) + '\')"'
    return result
