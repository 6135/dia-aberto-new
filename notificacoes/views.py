
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


def EnviarNotificacao(request):
    return render(request, 'notificacoes/enviar_notificacao.html')


def DetalhesNotificacao(request, pk):
    # envio_notificacao = get_object_or_404(models.Envionotificacao, pk=pk)
    notificacao = get_object_or_404(models.Notificacao, pk=pk)
    return render(request, 'notificacoes/detalhes_notificacao.html', {
        # 'envio_notificacao': envio_notificacao
        'notificacao': notificacao
    })


# # Ver detalhes de uma notificação automática

# def detalhes_notificacao_automatica(request, id):
#     notificacao = NotificacaoAutomatica.objects.get(id=id)
#     if notificacao == None:
#         return redirect("utilizadores:mensagem",5)
#     return render(request, 'notificacoes/detalhes_notificacao_automatica.html', {
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




