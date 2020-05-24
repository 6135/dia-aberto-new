from django import template
from utilizadores.models import *
from notificacoes.models import *

register = template.Library()



@register.filter(name='get_notificacoes') 
def get_notificacoes(user, filtro):
    if filtro == "Todas":
        return Notificacao.objects.all()  
    elif filtro == "False":
        return Notificacao.objects.filter(lida=False)
    else:
        return Notificacao.objects.filter(lida=True)  

