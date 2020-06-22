from django.http import HttpResponse
from .models import *
from utilizadores.models import *
from configuracao.models import *
from coordenadores.models import *
from atividades.models import *
import math

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import *
from django.conf import settings
from django.contrib.auth.models import Group

from django.core.paginator import Paginator

from notifications.signals import notify
from django.utils import timezone

from datetime import datetime, timedelta

from .forms import *


# Apagar uma notificação automática

def apagar_notificacao_automatica(request, id ,nr):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    notificacao = Notificacao.objects.get(id=nr)
    if notificacao == None:
        return redirect("utilizadores:mensagem", 5)
    notificacao.delete()
    x = 0 
    nr = 0  
    if id == 1:
        notificacoes = user.notifications.unread().order_by('-id') 
    elif id ==2:
        notificacoes = user.notifications.read().order_by('-id') 
    elif id == 3:
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=False).order_by('-id')
    elif id ==4:    
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=True).order_by('-id')
    elif id == 5:
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="info").order_by('-id')
    elif id ==6:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="warning").order_by('-id')
    elif id ==7: 
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="error").order_by('-id')
    elif id ==8:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="success").order_by('-id')
    else:
        notificacoes = user.notifications.all().order_by('-id')
    
    x = len(notificacoes)
    if nr!=0:
        notificacao = Notificacao.objects.get(id=nr)
        if notificacao == None:
            return redirect("notificacoes:sem-notificacoes", 10) 
    else:
        if x>0:
            notificacao = notificacoes[0]
        else:
            return redirect("notificacoes:sem-notificacoes", 10)    
    nr_notificacoes_por_pagina = 15
    paginator= Paginator(notificacoes,nr_notificacoes_por_pagina)
    page=request.GET.get('page')
    notificacoes = paginator.get_page(page)
    total = x
    if notificacao != None:
        notificacao.unread = False
        notificacao.save()
    else:
        return redirect("utilizadores:mensagem", 5)
    return render(request, 'notificacoes/detalhes_notificacao_automatica.html', {
        'atual': notificacao, 'notificacoes':notificacoes,'categoria':id,'total':total
    })

# Apagar notificacoes de um utilizadore por categorias


def limpar_notificacoes(request, id):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    if id == 1:
        notificacoes = user.notifications.unread() 
    elif id ==2:
        notificacoes = user.notifications.read() 
    elif id == 3:
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=False)
    elif id ==4:    
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=True)
    elif id == 5:
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="info")
    elif id ==6:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="warning")
    elif id ==7: 
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="error")
    elif id ==8:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="success")
    else:
        notificacoes = user.notifications.all()
    for x in notificacoes:
        x.delete()

    return redirect('notificacoes:categorias-notificacao-automatica',0,0)


# Marcar todas as notificações de um utilizador como lidas

def marcar_como_lida(request):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    user.notifications.mark_all_as_read(user)
    return redirect('notificacoes:categorias-notificacao-automatica',0,0)



# Página quando não existem notificacoes


def sem_notificacoes(request, id):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)

    return render(request, 'notificacoes/sem_notificacoes.html', {
        'categoria':id,
    })

# Ver notificações automáticas por categorias


def categorias_notificacao_automatica(request, id, nr):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    x = 0   
    if id == 1:
        notificacoes = user.notifications.unread().order_by('-id') 
    elif id ==2:
        notificacoes = user.notifications.read().order_by('-id') 
    elif id == 3:
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=False).order_by('-id')
    elif id ==4:    
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=True).order_by('-id')
    elif id == 5:
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="info").order_by('-id')
    elif id ==6:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="warning").order_by('-id')
    elif id ==7: 
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="error").order_by('-id')
    elif id ==8:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="success").order_by('-id')
    else:
        notificacoes = user.notifications.all().order_by('-id')
    
    x = len(notificacoes)
    if nr!=0:
        notificacao = Notificacao.objects.get(id=nr)
        if notificacao == None:
            return redirect("notificacoes:sem-notificacoes", 10) 
    else:
        if x>0:
            notificacao = notificacoes[0]
        else:
            return redirect("notificacoes:sem-notificacoes", 10)    
    nr_notificacoes_por_pagina = 15
    paginator= Paginator(notificacoes,nr_notificacoes_por_pagina)
    page=request.GET.get('page')
    notificacoes = paginator.get_page(page)
    total = x
    if notificacao != None:
        notificacao.unread = False
        notificacao.save()
    else:
        return redirect("utilizadores:mensagem", 5)
    return render(request, 'notificacoes/detalhes_notificacao_automatica.html', {
        'atual': notificacao, 'notificacoes':notificacoes,'categoria':id,'total':total
    })


# Mensagem pedido de cancelamento da tarefa

def enviar_notificacao_mensagem(request, id):
    tarefa = Tarefa.objects.get(id=id)
    nome = tarefa.coord.first_name+" "+tarefa.coord.last_name
    msg = "A enviar pedido de cancelamento de tarefa a "+nome
    return render(request=request,
                  template_name="colaboradores/enviar_notificacao.html",
                  context={"msg": msg})


# Envio de notificação automatica

def enviar_notificacao_automatica(request, sigla, id):
    if request.user.is_authenticated:
        user_sender = get_user(request)
    elif sigla!="validarRegistosPendentes":
        return redirect('utilizadores:mensagem', 5)
    # Enviar notificacao ao cancelar tarefa - colaborador
    if sigla == "cancelarTarefa":
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Pedido de cancelamento da tarefa"
        descricao = "Foi feito um pedido de cancelamento da tarefa \"" + \
            tarefa.getDescription()+"\""
        user_recipient = Utilizador.objects.get(id=tarefa.coord.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                    target=None, level="error", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificacao ao enviar confirmação do cancelamento da tarefa - coordenador
    elif sigla == "confirmarCancelarTarefa":
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Confirmação do cancelamento da tarefa"
        descricao = "O cancelamento da sua tarefa \"" + \
            tarefa.getDescription()+"\" foi aprovado."
        user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                    target=None, level="success", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação ao enviar rejeicao do pedido de cancelamento da tarefa - coordenador
    elif sigla == "rejeitarCancelarTarefa":
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Pedido de cancelamento da tarefa rejeitado"
        descricao = "O pedido de cancelamento da tarefa \"" + \
            tarefa.getDescription()+"\" foi rejeitado."
        user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                    target=None, level="warning", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação atividade confirmada - professor universitario
    elif sigla == "confirmarAtividade":
        atividade = Atividade.objects.get(id=id)
        titulo = "Confirmação da atividade proposta"
        descricao = "A sua proposta de atividade \""+atividade.nome+"\" foi aceite."
        user_recipient = Utilizador.objects.get(
            id=atividade.professoruniversitarioutilizadorid.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=None,
                    target=atividade, level="success", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação atividade rejeitada - professor universitario
    elif sigla == "rejeitarAtividade":
        atividade = Atividade.objects.get(id=id)
        titulo = "Rejeição da atividade proposta"
        descricao = "A sua proposta de atividade "+atividade.nome+" foi rejeitada."
        user_recipient = Utilizador.objects.get(
            id=atividade.professoruniversitarioutilizadorid.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=None,
                    target=atividade, level="error", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificacao tarefa atribuida - colaborador
    elif sigla == "tarefaAtribuida":
        tarefa = Tarefa.objects.get(id=id)
        if tarefa.estado != "naoAtribuida":
            titulo = "Atribuição de uma tarefa"
            descricao = "Foi lhe atribuida a tarefa \""+tarefa.getDescription()+"\""
            user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
            notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                        target=None, level="success", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação tarefa apagada - colaborador
    elif sigla == "tarefaApagada":
        titulo = "Foi apagada uma tarefa"
        tarefa = Tarefa.objects.get(id=id)
        descricao = "Foi apagada a tarefa \""+tarefa.getDescription() + \
            "\", por esse motivo a tarefa deixou de lhe estar atribuída."
        user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                    target=None, level="warning", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação tarefa alterada - colaborador
    elif sigla == "tarefaAlterada":
        tarefa = Tarefa.objects.get(id=id)
        if tarefa.estado != "naoAtribuida":
            titulo = "Alteração de uma tarefa"
            descricao = "Foi alterada a tarefa \""+tarefa.getDescription()+"\""
            user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
            notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                        target=None, level="info", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação atividade apagada - coordenador
    elif sigla == "atividadeApagada":
        titulo = "Foi apagada uma atividade"
        atividade = Atividade.objects.get(id=id)
        descricao = "Foi apagada a atividade \""+atividade.nome+"\""
        user_recipient = Utilizador.objects.get(
            id=atividade.get_coord().id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=None,
                    target=None, level="warning", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação atividade alterada - coordenador
    elif sigla == "atividadeAlterada":
        titulo = "Foi alterada uma atividade"
        atividade = Atividade.objects.get(id=id)
        descricao = "Foi feita uma alteração na atividade \""+atividade.nome+"\""
        user_recipient = Utilizador.objects.get(
            id=atividade.get_coord().id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=None,
                    target=atividade, level="warning", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação quando há registo de utilizador por validar - administrador e ao coordenador ( 5 dias depois de criado se ainda tiver pendente
    elif sigla == "validarRegistosPendentes":  # timezone.now() + timedelta(days=5)
        titulo = "Validação de registos de utilizadores pendentes"
        descricao = "Foram feitos registos de utilizadores na plataforma que necessitam de ser validados."
        administradores = Administrador.objects.all()
        user_sender = Utilizador.objects.get(id=id)
        for x in administradores:
            user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
            info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                              descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "register "+str(id) , lido = False)
            info.save()
        if user_sender.getProfile() != "Administrador":
            coordenadores = Coordenador.objects.filter(faculdade=Unidadeorganica.objects.get(id=user_sender.getUser().faculdade.id)) 
            for x in coordenadores: 
                user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
                info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                                descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "register "+str(id) , lido = False)
                info.save()
    # Enviar notificação quando há alterações de perfil de utilizador por validar - administrador e ao coordenador ( 5 dias depois de alterado se ainda tiver pendente )
    elif sigla == "validarAlteracoesPerfil":  # timezone.now() + timedelta(days=5)
        titulo = "Alterações de perfil de utilizadores por validar"
        descricao = "Foram feitas alterações de perfil de utilizadores que necessitam de ser validadas."
        administradores = Administrador.objects.all()
        user_sender = Utilizador.objects.get(id=id)
        for x in administradores:
            user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
            info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                              descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "profile "+str(id) , lido = False)
            info.save()
        if user_sender.getProfile() != "Administrador":
            coordenadores = Coordenador.objects.filter(faculdade=Unidadeorganica.objects.get(id=user_sender.getUser().faculdade.id)) 
            for x in coordenadores: 
                user_recipient = Utilizador.objects.get(id=x.id)
                info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                                descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "profile "+str(id) , lido = False)
                info.save()
    # Enviar notificação atividades por validar pendentes - coordenador (5 dias depois de criada a atividade se ainda tiver pendente)
    elif sigla == "validarAtividades":
        titulo = "Existem atividades por validar"
        atividade = Atividade.objects.get(id=id)
        descricao = "Foram criadas propostas de atividades que têm de ser validadas."
        user_recipient = Utilizador.objects.get(
            id=atividade.get_coord().id)
        user_sender = Utilizador.objects.get(id=user_sender.id)
        info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                              descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "atividade "+str(id) , lido = False)
        info.save()


######################################################### Mensagens #####################################################


def escolher_tipo(request):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    return render(request, 'notificacoes/escolher_tipo_mensagem.html')


def concluir_envio(request):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    return render(request, 'notificacoes/concluir_envio.html')

# Criar uma nova mensagem

def criar_mensagem(request, id):
    if request.user.is_authenticated: 
        user = get_user(request) 
        user = Utilizador.objects.get(id=user.id)
        if user.getProfile()=="Coordenador" or user.getProfile()=="Colaborador" or user.getProfile()=="ProfessorUniversitario" :
            return redirect('notificacoes:criar-mensagem-uo', id) 
        elif user.getProfile()=="Administrador":
            return redirect('notificacoes:criar-mensagem-admin', id) 
        elif user.getProfile()=="Participante":
            return redirect('notificacoes:criar-mensagem-participante', id) 
        else:
            return redirect('utilizadores:mensagem',5 ) 
    else:
        return redirect('utilizadores:mensagem', 5)      



# Criar uma nova mensagem por um colaborador, coordenador ou docente

def criar_mensagem_participante(request, id):
    msg = False
    if request.user.is_authenticated: 
        user = get_user(request) 
        user = Utilizador.objects.get(id=user.id)
    else:
        return redirect('utilizadores:mensagem', 5)      
           
    if request.method == "POST":
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualParticipante(request.POST)
        elif tipo == 1:
            form = MensagemFormGrupoParticipante(request.POST)
        else:
            return redirect("utilizadores:mensagem",5)
        if form.is_valid():
            titulo = form.cleaned_data.get('titulo')
            mensagem = form.cleaned_data.get('mensagem')
            if tipo == 0:
                email = form.cleaned_data.get('email')
                user_recipient = Utilizador.objects.get(email=email)
                info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "individual "+user_recipient.getProfile() , lido = False)
                info.save()
                mensagem1 = MensagemEnviada(mensagem_id=info.id)
                mensagem1.save()
                mensagem2 = MensagemRecebida(mensagem_id=info.id)
                mensagem2.save()
            elif tipo == 1:
                tipo_utilizadores = request.POST.get('filtro_tipo')
                if tipo_utilizadores == "Administrador":
                    utilizadores = Administrador.objects.all()    
                else:
                    return redirect("utilizadores:mensagem",5)
                
                for x in utilizadores:
                    user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
                    info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                    descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "grupo "+user_recipient.getProfile() , lido = False)
                    info.save()
                    mensagem = MensagemRecebida(mensagem_id=info.id)
                    mensagem.save()  
                mensagem1 = MensagemEnviada(mensagem_id=info.id)
                mensagem1.save()    
            return redirect("notificacoes:concluir-envio")
        else:
            msg = True
            if tipo == 0:
                return render(request=request,
                    template_name="notificacoes/enviar_notificacao.html",
                    context={"form": form,"msg":msg,})
            elif tipo == 1:    
                form_group = UtilizadorFiltroParticipante(request.POST)
                return render(request=request,
                            template_name="notificacoes/enviar_para_grupo.html",
                            context={"form": form,"form_group":form_group,"msg":msg,})
    else:
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualParticipante()
            return render(request=request,
                  template_name="notificacoes/enviar_notificacao.html",
                  context={"form": form,"msg":msg,})
        elif tipo == 1:
            formFilter = UtilizadorFiltroParticipante()
            form = MensagemFormGrupoParticipante()
            return render(request=request,
                  template_name="notificacoes/enviar_para_grupo.html",
                  context={"form": form,"form_group":formFilter,"msg":msg,})
        else:
            return redirect("utilizadores:mensagem",5)


# Criar uma nova mensagem por um colaborador, coordenador ou docente

def criar_mensagem_uo(request, id):
    msg = False
    if request.user.is_authenticated: 
        user = get_user(request) 
        user = Utilizador.objects.get(id=user.id)
    else:
        return redirect('utilizadores:mensagem', 5)      
           
    if request.method == "POST":
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualUO(request.POST)
        elif tipo == 1:
            form = MensagemFormGrupoUO(request.POST)
        else:
            return redirect("utilizadores:mensagem",5)
        if form.is_valid():
            titulo = form.cleaned_data.get('titulo')
            mensagem = form.cleaned_data.get('mensagem')
            if tipo == 0:
                email = form.cleaned_data.get('email')
                user_recipient = Utilizador.objects.get(email=email)
                if user_recipient.emailValidoUO(user.getUser().faculdade) == False:
                    msg_erro = "Apenas pode ser enviada mensagem a coordenadores, colaboradores ou professores universitários da mesma unidade orgânica ou a administradores"
                    msg = True
                    erro = True
                    return render(request=request,
                        template_name="notificacoes/enviar_notificacao.html",
                        context={"form": form,"msg":msg,"msg_erro":msg_erro, "erro":erro})
                else:        
                    info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                    descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "individual "+user_recipient.getProfile() , lido = False)
                    info.save()
                    mensagem1 = MensagemEnviada(mensagem_id=info.id)
                    mensagem1.save()
                    mensagem2 = MensagemRecebida(mensagem_id=info.id)
                    mensagem2.save()
            elif tipo == 1:
                tipo_utilizadores = request.POST.get('filtro_tipo')
                if tipo_utilizadores == "ProfessorUniversitario":
                    utilizadores = ProfessorUniversitario.objects.filter(faculdade=user.getUser().faculdade)
                elif tipo_utilizadores == "Coordenador":
                    utilizadores = Coordenador.objects.filter(faculdade=user.getUser().faculdade)
                elif tipo_utilizadores == "Colaborador":
                    utilizadores = Colaborador.objects.filter(faculdade=user.getUser().faculdade)
                elif tipo_utilizadores == "Administrador":
                    utilizadores = Administrador.objects.filter()    
                else:
                    return redirect("utilizadores:mensagem",5)
                
                for x in utilizadores:
                    user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
                    info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                    descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "grupo "+user_recipient.getProfile() , lido = False)
                    info.save()
                    mensagem = MensagemRecebida(mensagem_id=info.id)
                    mensagem.save()  
                mensagem1 = MensagemEnviada(mensagem_id=info.id)
                mensagem1.save()    
            return redirect("notificacoes:concluir-envio")
        else:
            msg = True
            if tipo == 0:
                return render(request=request,
                    template_name="notificacoes/enviar_notificacao.html",
                    context={"form": form,"msg":msg,})
            elif tipo == 1:    
                form_group = UtilizadorFiltroUO(request.POST)
                return render(request=request,
                            template_name="notificacoes/enviar_para_grupo.html",
                            context={"form": form,"form_group":form_group,"msg":msg,})
    else:
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualUO()
            return render(request=request,
                  template_name="notificacoes/enviar_notificacao.html",
                  context={"form": form,"msg":msg,})
        elif tipo == 1:
            formFilter = UtilizadorFiltroUO()
            form = MensagemFormGrupoUO()
            return render(request=request,
                  template_name="notificacoes/enviar_para_grupo.html",
                  context={"form": form,"form_group":formFilter,"msg":msg,})
        else:
            return redirect("utilizadores:mensagem",5)

# Criar uma nova mensagem por um administrador

def criar_mensagem_admin(request, id):
    msg = False
    if request.user.is_authenticated: 
        user = get_user(request) 
        user = Utilizador.objects.get(id=user.id)
    else:
        return redirect('utilizadores:mensagem', 5)      
           
    if request.method == "POST":
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualAdmin(request.POST)
        elif tipo == 1:
            form = MensagemFormGrupoAdmin(request.POST)
        else:
            return redirect("utilizadores:mensagem",5)
        if form.is_valid():
            titulo = form.cleaned_data.get('titulo')
            mensagem = form.cleaned_data.get('mensagem')
            if tipo == 0:
                email = form.cleaned_data.get('email')
                user_recipient = Utilizador.objects.get(email=email)
                info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "individual "+user_recipient.getProfile() , lido = False)
                info.save()
                mensagem1 = MensagemEnviada(mensagem_id=info.id)
                mensagem1.save()
                mensagem2 = MensagemRecebida(mensagem_id=info.id)
                mensagem2.save()
            elif tipo == 1:
                tipo_utilizadores = request.POST.get('filtro_tipo')
                if tipo_utilizadores == "Participante":
                    utilizadores = Participante.objects.all()
                elif tipo_utilizadores == "ProfessorUniversitario":
                    utilizadores = ProfessorUniversitario.objects.all()
                elif tipo_utilizadores == "Coordenador":
                    utilizadores = Coordenador.objects.all()
                elif tipo_utilizadores == "Colaborador":
                    utilizadores = Colaborador.objects.all()
                elif tipo_utilizadores == "Administrador":
                    utilizadores = Administrador.objects.all()    
                else:
                    return redirect("utilizadores:mensagem",5)
                
                for x in utilizadores:
                    user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
                    info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                    descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "grupo "+user_recipient.getProfile() , lido = False)
                    info.save()
                    mensagem = MensagemRecebida(mensagem_id=info.id)
                    mensagem.save()  
                mensagem1 = MensagemEnviada(mensagem_id=info.id)
                mensagem1.save()    
            return redirect("notificacoes:concluir-envio")
        else:
            msg = True
            if tipo == 0:
                return render(request=request,
                    template_name="notificacoes/enviar_notificacao.html",
                    context={"form": form,"msg":msg,})
            elif tipo == 1:    
                form_group = UtilizadorFiltro(request.POST)
                return render(request=request,
                            template_name="notificacoes/enviar_para_grupo.html",
                            context={"form": form,"form_group":form_group,"msg":msg,})
    else:
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualAdmin()
            return render(request=request,
                  template_name="notificacoes/enviar_notificacao.html",
                  context={"form": form,"msg":msg,})
        elif tipo == 1:
            formFilter = UtilizadorFiltro()
            form = MensagemFormGrupoAdmin()
            return render(request=request,
                  template_name="notificacoes/enviar_para_grupo.html",
                  context={"form": form,"form_group":formFilter,"msg":msg,})
        else:
            return redirect("utilizadores:mensagem",5)
    

# Apagar uma mensagem

def apagar_mensagem(request, id ,nr):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    notificacao = Notificacao.objects.get(id=nr)
    if notificacao == None:
        return redirect("utilizadores:mensagem", 5)
    notificacao.delete()
    x = 0 
    nr = 0  
    if id == 1:
        notificacoes = user.notifications.unread().order_by('-id') 
    elif id ==2:
        notificacoes = user.notifications.read().order_by('-id') 
    elif id == 3:
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=False).order_by('-id')
    elif id ==4:    
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=True).order_by('-id')
    elif id == 5:
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="info").order_by('-id')
    elif id ==6:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="warning").order_by('-id')
    elif id ==7: 
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="error").order_by('-id')
    elif id ==8:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="success").order_by('-id')
    else:
        notificacoes = user.notifications.all().order_by('-id')
    
    x = len(notificacoes)
    if nr!=0:
        notificacao = Notificacao.objects.get(id=nr)
        if notificacao == None:
            return redirect("notificacoes:sem-notificacoes", 10) 
    else:
        if x>0:
            notificacao = notificacoes[0]
        else:
            return redirect("notificacoes:sem-notificacoes", 10)    
    nr_notificacoes_por_pagina = 15
    paginator= Paginator(notificacoes,nr_notificacoes_por_pagina)
    page=request.GET.get('page')
    notificacoes = paginator.get_page(page)
    total = x
    if notificacao != None:
        notificacao.unread = False
        notificacao.save()
    else:
        return redirect("utilizadores:mensagem", 5)
    return render(request, 'notificacoes/detalhes_mensagens.html', {
        'atual': notificacao, 'notificacoes':notificacoes,'categoria':id,'total':total
    })

# Apagar mensagens por categorias de um dado utilizador


def limpar_mensagens(request, id):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    if id == 1:
        notificacoes = user.notifications.unread() 
    elif id ==2:
        notificacoes = user.notifications.read() 
    elif id == 3:
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=False)
    elif id ==4:    
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=True)
    elif id == 5:
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="info")
    elif id ==6:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="warning")
    elif id ==7: 
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="error")
    elif id ==8:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="success")
    else:
        notificacoes = user.notifications.all()
    for x in notificacoes:
        x.delete()

    return redirect('notificacoes:categorias-notificacao-automatica',0,0)


# Marcar todas as mensagens de um utilizador como lidas

def mensagem_como_lida(request):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    user.notifications.mark_all_as_read(user)
    return redirect('notificacoes:categorias-notificacao-automatica',0,0)



# Página quando não existem mensagens


def sem_mensagens(request, id):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)

    return render(request, 'notificacoes/sem_mensagens.html', {
        'categoria':id,
    })

# Ver mensagens por categorias


def detalhes_mensagens(request, id, nr):
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    x = 0   
    if id == 1:
        notificacoes = user.notifications.unread().order_by('-id') 
    elif id ==2:
        notificacoes = user.notifications.read().order_by('-id') 
    elif id == 3:
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=False).order_by('-id')
    elif id ==4:    
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=True).order_by('-id')
    elif id == 5:
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="info").order_by('-id')
    elif id ==6:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="warning").order_by('-id')
    elif id ==7: 
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="error").order_by('-id')
    elif id ==8:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="success").order_by('-id')
    else:
        notificacoes = user.notifications.all().order_by('-id')
    
    x = len(notificacoes)
    if nr!=0:
        notificacao = Notificacao.objects.get(id=nr)
        if notificacao == None:
            return redirect("notificacoes:sem-notificacoes", 10) 
    else:
        if x>0:
            notificacao = notificacoes[0]
        else:
            return redirect("notificacoes:sem-notificacoes", 10)    
    nr_notificacoes_por_pagina = 15
    paginator= Paginator(notificacoes,nr_notificacoes_por_pagina)
    page=request.GET.get('page')
    notificacoes = paginator.get_page(page)
    total = x
    if notificacao != None:
        notificacao.unread = False
        notificacao.save()
    else:
        return redirect("utilizadores:mensagem", 5)
    return render(request, 'notificacoes/detalhes_mensagens.html', {
        'atual': notificacao, 'notificacoes':notificacoes,'categoria':id,'total':total
    })

