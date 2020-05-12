from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from utilizadores.models import *
from configuracao.models import *
from coordenadores.models import *
from django.shortcuts import redirect
from .forms import *
from django.contrib.auth import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group


# Envio de notificação automática e em alguns casos podera haver redirecionamento para uma pagina a informar que a notificação automática foi enviada

def enviar_notificacao_automatica(request, sigla, id, user_id):
    today = datetime.now(timezone.utc)
    user = Utilizador.objects.get(id=user_id)
    if sigla == "cancelarTarefa"# Enviar notificação ao cancelar tarefa - colaborador
        msg = "A enviar notificação a "+user.name+" a solicitar o cancelamento da tarefa"
        tipo = 1
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Pedido de cancelamento da tarefa"
        descricao = "Foi feito um pedido de cancelamento da tarefa "+tarefa.nome
    elif sigla == "confirmarCancelarTarefa" # Enviar notificação ao enviar confirmação do cancelamento da tarefa - coordenador
        msg = "A enviar notificação a "+user.name+" a confirmar o cancelamento da tarefa"
        tipo = 2
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Confirmação do cancelamento da tarefa"
        descricao = "O cancelamento da sua tarefa "+tarefa.nome+" foi aprovado"
    elif sigla == "confirmarAtividade" # Enviar notificação atividade confirmada - professor universitário
        msg = "A enviar notificação a "+user.name+" a informar que a atividade foi aceite"
        tipo = 3
        atividade = Atividade.objects.get(id=id)
        titulo = "Confirmação da atividade proposta"
        descricao = "A sua proposta de atividade "+atividade.nome+" foi aceite"
    elif sigla == "rejeitarAtividade"# Enviar notificação atividade rejeitada - professor universitário
        # msg = "A enviar notificação a "+user.name+" a informar que a atividade foi rejeitada"
        tipo = 4
        atividade = Atividade.objects.get(id=id)
        titulo = "Rejeição da atividade proposta"
        descricao = "A sua proposta de atividade "+atividade.nome+" foi rejeitada"
    elif sigla == "tarefaAtribuida"# Enviar notificação tarefa atribuida - colaborador
        # msg = "A enviar notificação a "+user.name+" a informar que lhe foi atribuída uma tarefa"
        tipo = 6
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Atribuição de uma tarefa"
        descricao = "Foi lhe atribuida a tarefa "+tarefa.nome
    elif sigla == "tarefaApagada" # Enviar notificação tarefa apagada - colaborador 
        tipo = 7
        titulo = "Atividade apagada"
        tarefa = Tarefa.objects.get(id=id)
        descricao = "Foi apagada a tarefa "+tarefa.nome
        novaNotificacao = NotificacaoAutomatica(titulo=titulo,descricao=descricao,criadoem=today ,recetor=user), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
        novaNotificacao.save()      
        return redirect("")
    elif sigla == "tarefaAlterada"# Enviar notificação tarefa alterada - colaborador
        tipo = 8
        tarefa = Tarefa.objects.get(id=id)
        descricao = "Foi alterada a tarefa "+tarefa.nome
        novaNotificacao = NotificacaoAutomatica(titulo=titulo,descricao=descricao,criadoem=today ,recetor=user), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
        novaNotificacao.save()      
        return redirect("")
    elif sigla == "atividadeAlterada"# Enviar notificação atividade apagada - coordenador
        tipo = 9
        titulo = "Atividade apagada"
        atividade = Atividade.objects.get(id=id)
        descricao = "Foi apagada a atividade"+tarefa.nome
        novaNotificacao = NotificacaoAutomatica(titulo=titulo,descricao=descricao,criadoem=today ,recetor=user), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
        novaNotificacao.save()      
        return redirect("")
    elif sigla == "validarRegistosPendentes" # Enviar notificação atividade alterada - coordenador
        tipo = 10
        titulo = "Alteração em uma atividade "
        atividade = Atividade.objects.get(id=id)
        descricao = "Foi feita uma alteração na atividade "+atividade.nome  
        novaNotificacao = NotificacaoAutomatica(titulo=titulo,descricao=descricao,criadoem=today ,recetor=user), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
        novaNotificacao.save()      
        return redirect("")
    elif sigla == "validarRegistosPendentes" # Enviar notificação quando há registo de utilizador por validar (5 dias antes do fim das inscrições) - administrador e ao coordenador
        tipo = 11
        titulo = "Validação de registos de utilizadores pendentes"
        descricao = "Existem registos de utilizadores por validar" 
        novaNotificacao = NotificacaoAutomatica(titulo=titulo,descricao=descricao,criadoem=today ,recetor=user), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
        novaNotificacao.save()      
        return redirect("")
    elif sigla == "validarAtividades" # Enviar notificação quando há atividades por validar (5 dias antes do fim das inscrições) - coordenador
        tipo = 5
        titulo = "Validação de atividades pendentes"
        descricao = "Existem atividades por validar" 
        novaNotificacao = NotificacaoAutomatica(titulo=titulo,descricao=descricao,criadoem=today ,recetor=user), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
        novaNotificacao.save()      
        return redirect("")


    novaNotificacao = NotificacaoAutomatica(titulo=titulo,descricao=descricao,criadoem=today ,recetor=user), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
    novaNotificacao.save()   


    return render(request=request,
                  template_name="notificacao/enviar_notificacao.html",
                  context={"msg": msg, "id":id, "tipo": tipo})



