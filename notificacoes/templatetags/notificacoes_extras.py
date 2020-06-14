from django import template
from utilizadores.models import *
from notificacoes.models import *

from distutils.version import StrictVersion  # pylint: disable=no-name-in-module,import-error

from django import get_version
from django.template import Library
from django.utils.html import format_html


from notifications.signals import notify


try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse  # pylint: disable=no-name-in-module,import-error

register = Library()


register = template.Library()



@register.filter(name='get_notificacoes') 
def get_notificacoes(user, filtro):
    if user.is_authenticated:    
        if filtro == "Todas":
            return user.notifications.all() 
        elif filtro == "False":
            return user.notifications.unread()
        else:
            return user.notifications.read()  
        
    else:
        return None


@register.filter(name='get_notificacoes_nr') 
def get_notificacoes_nr(user, filtro):
    if user.is_authenticated:    
        if filtro == "Todas":
            return len(user.notifications.all()) 
        elif filtro == "Novas":
            return len(user.notifications.unread())
        elif filtro == "Anteriores":
            return len(user.notifications.read())  
        else:
            return None    
        
    else:
        return None


@register.filter(name='nr_notificacoes') 
def nr_notificacoes(user):
    if not user:
        return 0
    return user.notifications.unread().count()