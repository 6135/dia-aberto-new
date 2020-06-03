from django import template
from ..models import Inscricao
from utilizadores.models import Participante

register = template.Library()

@register.filter
def inscrito(user):
    return Inscricao.objects.filter(participante=user.id).exists()

@register.filter
def inscricao(user):
    return Inscricao.objects.filter(participante=user.id).first().id