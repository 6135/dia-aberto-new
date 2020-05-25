
from django.http import HttpResponse
from .models import *
from utilizadores.models import *
from configuracao.models import *
from coordenadores.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group




from distutils.version import \
    StrictVersion  # pylint: disable=no-name-in-module,import-error

from django import get_version
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from dia_aberto import settings
from dia_aberto.settings import get_config
from notifications.utils import id2slug, slug2id
from swapper import load_model

Notificacao = load_model('notifications', 'Notificacao')

from django.http import JsonResponse  


class NotificacaoViewList(ListView):
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = settings.get_config()['PAGINATE_BY']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificacaoViewList, self).dispatch(
            request, *args, **kwargs)


class AllNotificationsList(NotificacaoViewList):
    """
    Index page for authenticated user
    """

    def get_queryset(self):
        if settings.get_config()['SOFT_DELETE']:
            qset = self.request.user.notifications.active()
        else:
            qset = self.request.user.notifications.all()
        return qset


class UnreadNotificationsList(NotificacaoViewList):

    def get_queryset(self):
        return self.request.user.notifications.unread()


@login_required
def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)
    return redirect('notifications:unread')


@login_required
def mark_as_read(request, slug=None):
    Notificacao_id = slug2id(slug)

    Notificacao = get_object_or_404(
        Notificacao, recipient=request.user, id=Notificacao_id)
    Notificacao.mark_as_read()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    return redirect('notifications:unread')


@login_required
def mark_as_unread(request, slug=None):
    Notificacao_id = slug2id(slug)

    Notificacao = get_object_or_404(
        Notificacao, recipient=request.user, id=Notificacao_id)
    Notificacao.mark_as_unread()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    return redirect('notifications:unread')


@login_required
def delete(request, slug=None):
    Notificacao_id = slug2id(slug)

    Notificacao = get_object_or_404(
        Notificacao, recipient=request.user, id=Notificacao_id)

    if settings.get_config()['SOFT_DELETE']:
        Notificacao.deleted = True
        Notificacao.save()
    else:
        Notificacao.delete()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    return redirect('notifications:all')


@never_cache
def live_unread_notification_count(request):
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'unread_count': 0
        }
    else:
        data = {
            'unread_count': request.user.notifications.unread().count(),
        }
    return JsonResponse(data)


@never_cache
def live_unread_notification_list(request):
    ''' Return a json with a unread Notificacao list '''
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'unread_count': 0,
            'unread_list': []
        }
        return JsonResponse(data)

    default_num_to_fetch = get_config()['NUM_TO_FETCH']
    try:
        # If they don't specify, make it 5.
        num_to_fetch = request.GET.get('max', default_num_to_fetch)
        num_to_fetch = int(num_to_fetch)
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:  # If casting to an int fails.
        num_to_fetch = default_num_to_fetch

    unread_list = []

    for Notificacao in request.user.notifications.unread()[0:num_to_fetch]:
        struct = model_to_dict(Notificacao)
        struct['slug'] = id2slug(Notificacao.id)
        if Notificacao.actor:
            struct['actor'] = str(Notificacao.actor)
        if Notificacao.target:
            struct['target'] = str(Notificacao.target)
        if Notificacao.action_object:
            struct['action_object'] = str(Notificacao.action_object)
        if Notificacao.data:
            struct['data'] = Notificacao.data
        unread_list.append(struct)
        if request.GET.get('mark_as_read'):
            Notificacao.mark_as_read()
    data = {
        'unread_count': request.user.notifications.unread().count(),
        'unread_list': unread_list
    }
    return JsonResponse(data)


@never_cache
def live_all_notification_list(request):
    ''' Return a json with a unread Notificacao list '''
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'all_count': 0,
            'all_list': []
        }
        return JsonResponse(data)

    default_num_to_fetch = get_config()['NUM_TO_FETCH']
    try:
        # If they don't specify, make it 5.
        num_to_fetch = request.GET.get('max', default_num_to_fetch)
        num_to_fetch = int(num_to_fetch)
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:  # If casting to an int fails.
        num_to_fetch = default_num_to_fetch

    all_list = []

    for Notificacao in request.user.notifications.all()[0:num_to_fetch]:
        struct = model_to_dict(Notificacao)
        struct['slug'] = id2slug(Notificacao.id)
        if Notificacao.actor:
            struct['actor'] = str(Notificacao.actor)
        if Notificacao.target:
            struct['target'] = str(Notificacao.target)
        if Notificacao.action_object:
            struct['action_object'] = str(Notificacao.action_object)
        if Notificacao.data:
            struct['data'] = Notificacao.data
        all_list.append(struct)
        if request.GET.get('mark_as_read'):
            Notificacao.mark_as_read()
    data = {
        'all_count': request.user.notifications.count(),
        'all_list': all_list
    }
    return JsonResponse(data)


def live_all_notification_count(request):
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'all_count': 0
        }
    else:
        data = {
            'all_count': request.user.notifications.count(),
        }
    return JsonResponse(data)


def EnviarNotificacao(request):
    return render(request, 'notifications/enviar_notificacao.html')


def DetalhesNotificacao(request, pk):
    # envio_notificacao = get_object_or_404(models.Envionotificacao, pk=pk)
    notificacao = get_object_or_404(models.Notificacao, pk=pk)
    return render(request, 'notifications/detalhes_notificacao.html', {
        # 'envio_notificacao': envio_notificacao
        'notificacao': notificacao
    })


# # Ver detalhes de uma notificação automática

# def detalhes_notificacao_automatica(request, id):
#     notificacao = NotificacaoAutomatica.objects.get(id=id)
#     if notificacao == None:
#         return redirect("utilizadores:mensagem",5)
#     return render(request, 'notifications/detalhes_notificacao_automatica.html', {
#         'notificacao': notificacao
#     })

# # Envio de notificação automática

# def enviar_notificacao_automatica(request, sigla, id, user_id):
#     today = datetime.now(timezone.utc)
#     user = Utilizador.objects.get(id=user_id)
#     if sigla == "cancelarTarefa":  # Enviar notificação ao cancelar tarefa - colaborador
#         tarefa = Tarefa.objects.get(id=id)
#         titulo = "Pedido de cancelamento da tarefa"
#         descricao = "Foi feito um pedido de cancelamento da tarefa "+tarefa.nome
#         novaNotificacao = NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")
#     # Enviar notificação ao enviar confirmação do cancelamento da tarefa - coordenador
#     elif sigla == "confirmarCancelarTarefa":
#         tarefa = Tarefa.objects.get(id=id)
#         titulo = "Confirmação do cancelamento da tarefa"
#         descricao = "O cancelamento da sua tarefa "+tarefa.nome+" foi aprovado"
#         novaNotificacao = NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")
#     # Enviar notificação atividade confirmada - professor universitário
#     elif sigla == "confirmarAtividade":
#         atividade = Atividade.objects.get(id=id)
#         titulo = "Confirmação da atividade proposta"
#         descricao = "A sua proposta de atividade "+atividade.nome+" foi aceite"
#         novaNotificacao = NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")
#     # Enviar notificação atividade rejeitada - professor universitário
#     elif sigla == "rejeitarAtividade":
#         atividade = Atividade.objects.get(id=id)
#         titulo = "Rejeição da atividade proposta"
#         descricao = "A sua proposta de atividade "+atividade.nome+" foi rejeitada"
#         novaNotificacao = NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")
#     elif sigla == "tarefaAtribuida":  # Enviar notificação tarefa atribuida - colaborador
#         tarefa = Tarefa.objects.get(id=id)
#         titulo = "Atribuição de uma tarefa"
#         descricao = "Foi lhe atribuida a tarefa "+tarefa.nome
#         novaNotificacao = NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")

#     elif sigla == "tarefaApagada":  # Enviar notificação tarefa apagada - colaborador
#         titulo = "Atividade apagada"
#         tarefa = Tarefa.objects.get(id=id)
#         descricao = "Foi apagada a tarefa "+tarefa.nome
#         novaNotificacao = NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")
#     elif sigla == "tarefaAlterada":  # Enviar notificação tarefa alterada - colaborador
#         tarefa=Tarefa.objects.get(id = id)
#         descricao="Foi alterada a tarefa "+tarefa.nome
#         novaNotificacao=NotificacaoAutomatica(titulo = titulo, descricao = descricao, criadoem = today, recetor = user)
#         novaNotificacao.save()
#         return redirect("")
#     # Enviar notificação atividade apagada - coordenador
#     elif sigla == "atividadeAlterada":
#         titulo="Atividade apagada"
#         atividade=Atividade.objects.get(id=id)
#         descricao="Foi apagada a atividade"+tarefa.nome
#         novaNotificacao=NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")
#     # Enviar notificação atividade alterada - coordenador
#     elif sigla == "validarRegistosPendentes":
#         titulo="Alteração em uma atividade "
#         atividade=Atividade.objects.get(id=id)
#         descricao="Foi feita uma alteração na atividade "+atividade.nome
#         novaNotificacao=NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")
#     # Enviar notificação quando há registo de utilizador por validar (5 dias antes do fim das inscrições) - administrador e ao coordenador
#     elif sigla == "validarRegistosPendentes":
#         titulo="Validação de registos de utilizadores pendentes"
#         descricao="Existem registos de utilizadores por validar"
#         novaNotificacao=NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")
#     # Enviar notificação quando há atividades por validar (5 dias antes do fim das inscrições) - coordenador
#     elif sigla == "validarAtividades":
#         titulo="Validação de atividades pendentes"
#         descricao="Existem atividades por validar"
#         novaNotificacao=NotificacaoAutomatica(titulo=titulo,lida=False, descricao=descricao, criadoem=today, recetor=user, sigla=sigla)
#         novaNotificacao.save()
#         return redirect("")




