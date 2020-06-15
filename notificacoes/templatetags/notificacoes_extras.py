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



@register.filter(name='notificacoes_lidas') 
def notificacoes_lidas(user):
    if user.is_authenticated:    
            return user.notifications.read()  
    else:
        return None


@register.filter(name='nr_notificacoes_lidas') 
def nr_notificacoes(user):
    if not user:
        return 0
    return user.notifications.read().count()

@register.filter(name='nr_notificacoes') 
def nr_notificacoes(user):
    if not user:
        return 0
    return user.notifications.all().count()

# Requires vanilla-js framework - http://vanilla-js.com/
@register.simple_tag
def register_notify(badge_class='live_notify_badge',  # pylint: disable=too-many-arguments,missing-docstring
                              menu_class='notification_list',
                              refresh_period=15,
                              callbacks='',
                              api_name='list',
                              fetch=50):
    refresh_period = int(refresh_period) * 1000

    if api_name == 'list':
        api_url = reverse('notifications:live_unread_notification_list')
    elif api_name == 'count':
        api_url = reverse('notifications:live_unread_notification_count')
    else:
        return ""
    definitions = """
        notify_badge_class='{badge_class}';
        notify_menu_class='{menu_class}';
        notify_api_url='{api_url}';
        notify_fetch_count='{fetch_count}';
        notify_unread_url='{unread_url}';
        notify_mark_all_unread_url='{mark_all_unread_url}';
        notify_refresh_period={refresh};
    """.format(
        badge_class=badge_class,
        menu_class=menu_class,
        refresh=refresh_period,
        api_url=api_url,
        unread_url=reverse('notifications:unread'),
        mark_all_unread_url=reverse('notifications:mark_all_as_read'),
        fetch_count=fetch
    )

    script = "<script>" + definitions
    for callback in callbacks.split(','):
        script += "register_notifier(" + callback + ");"
    script += "</script>"
    return format_html(script)


@register.simple_tag(takes_context=True)
def live_notify_badge(context, badge_class='live_notify_badge'):
    user = user_context(context)
    if not user:
        return ''

    return user.notifications.unread().count()


@register.simple_tag
def notification_list(list_class='notification_list'):
    html = "<ul class='{list_class}'></ul>".format(list_class=list_class)
    return format_html(html)

