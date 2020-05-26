from django import template
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.filter
def colab_none(colab):
    if colab is None or str(colab) == 'None':
        return 'N/A'
    else:
        return colab