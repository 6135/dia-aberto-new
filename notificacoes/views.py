
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


from notifications.signals import notify
from django.utils import timezone




def EnviarNotificacao(request):
    return render(request, 'notificacoes/enviar_notificacao.html')


def DetalhesNotificacao(request, pk):
    # envio_notificacao = get_object_or_404(models.Envionotificacao, pk=pk)
    notificacao = get_object_or_404(models.Notificacao, pk=pk)
    return render(request, 'notificacoes/detalhes_notificacao.html', {
        # 'envio_notificacao': envio_notificacao
        'notificacao': notificacao
    })


# Apagar uma notificação automática

def apagar_notificacao_automatica(request, id):
    notificacao = Notificacao.objects.get(id=id)
    notificacao.deleted = True
    notificacao.save()
    if notificacao == None:
        return redirect("utilizadores:mensagem",5)
    return render(request, 'notificacoes/detalhes_notificacao_automatica.html', {
        'notificacao': notificacao
    })

# Ver detalhes de uma notificação automática
def detalhes_notificacao_automatica(request, id):
    notificacao = Notificacao.objects.get(id=id)
    notificacao.unread = False
    notificacao.save()
    if notificacao == None:
        return redirect("utilizadores:mensagem",5)
    return render(request, 'notificacoes/detalhes_notificacao_automatica.html', {
        'notificacao': notificacao
    })


#Mensagem pedido de cancelamento da tarefa
def enviar_notificacao_mensagem(request,id): 
    tarefa = Tarefa.objects.get(id=id)
    nome = tarefa.coord.first_name+" "+tarefa.coord.last_name
    msg="A enviar pedido de cancelamento de tarefa a "+nome
    return render(request=request,
                  template_name="colaboradores/enviar_notificacao.html",
                  context={"msg": msg})


# Envio de notificação automática
def enviar_notificacao_automatica(sender, sigla, id ):
    user_sender = Utilizador.objects.get(id=sender)
    # Enviar notificação ao cancelar tarefa - colaborador
    if sigla == "cancelarTarefa":  
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Pedido de cancelamento da tarefa"
        descricao = "Foi feito um pedido de cancelamento da tarefa "+tarefa.nome
        user_recipient = Utilizador.objects.get(id=tarefa.coord.id)
        notify.send(sender=user_sender, recipient=user_recipient,verb=descricao, action_object=None, target=None, level="error",description=titulo,public=False, timestamp=timezone.now())
    # Enviar notificação ao enviar confirmação do cancelamento da tarefa - coordenador
    elif sigla == "confirmarCancelarTarefa":
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Confirmação do cancelamento da tarefa"
        descricao = "O cancelamento da sua tarefa "+tarefa.nome+" foi aprovado"
        
        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")
    # Enviar notificação atividade confirmada - professor universitário
    elif sigla == "confirmarAtividade":
        atividade = Atividade.objects.get(id=id)
        titulo = "Confirmação da atividade proposta"
        descricao = "A sua proposta de atividade "+atividade.nome+" foi aceite"
        
        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")
    # Enviar notificação atividade rejeitada - professor universitário
    elif sigla == "rejeitarAtividade":
        atividade = Atividade.objects.get(id=id)
        titulo = "Rejeição da atividade proposta"
        descricao = "A sua proposta de atividade "+atividade.nome+" foi rejeitada"
        
        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")
    elif sigla == "tarefaAtribuida":  # Enviar notificação tarefa atribuida - colaborador
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Atribuição de uma tarefa"
        descricao = "Foi lhe atribuida a tarefa "+tarefa.nome
        
        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")

    elif sigla == "tarefaApagada":  # Enviar notificação tarefa apagada - colaborador
        titulo = "Atividade apagada"
        tarefa = Tarefa.objects.get(id=id)
        descricao = "Foi apagada a tarefa "+tarefa.nome
        
        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")
    elif sigla == "tarefaAlterada":  # Enviar notificação tarefa alterada - colaborador
        tarefa=Tarefa.objects.get(id = id)
        descricao="Foi alterada a tarefa "+tarefa.nome
        novaNotificacao=NotificacaoAutomatica(titulo = titulo, descricao = descricao, criadoem = today, recetor = user)
        novaNotificacao.save()
        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")
    # Enviar notificação atividade apagada - coordenador
    elif sigla == "atividadeAlterada":
        titulo="Atividade apagada"
        atividade=Atividade.objects.get(id=id)
        descricao="Foi apagada a atividade"+tarefa.nome

        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")
    # Enviar notificação atividade alterada - coordenador
    elif sigla == "validarRegistosPendentes":
        titulo="Alteração em uma atividade "
        atividade=Atividade.objects.get(id=id)
        descricao="Foi feita uma alteração na atividade "+atividade.nome

        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")
    # Enviar notificação quando há registo de utilizador por validar (5 dias antes do fim das inscrições) - administrador e ao coordenador
    elif sigla == "validarRegistosPendentes":
        titulo="Validação de registos de utilizadores pendentes"
        descricao="Existem registos de utilizadores por validar"

        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")
    # Enviar notificação quando há atividades por validar (5 dias antes do fim das inscrições) - coordenador
    elif sigla == "validarAtividades":
        titulo="Validação de atividades pendentes"
        descricao="Existem atividades por validar"

        notify.send(sender=user, recipient=user,verb="oi", action_object=None, target=None, level="info",description="Foi feito um pedido de cancelamento da tarefa ",public=False, timestamp=timezone.now(),titulo="tiago")




