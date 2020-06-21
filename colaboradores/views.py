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

from django.core.paginator import Paginator

from notificacoes import views

# Funcionalidade de consultar tarefas do colaborador atual, funcionalidades de filtros para a a consulta das tarefas

def consultar_tarefas(request):
        
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        else:
            return redirect('utilizadores:mensagem',5)
    else:
        return redirect('utilizadores:mensagem',5)  


    if request.method == 'POST':
        formFilter = TarefaFiltro(request.POST)
        current = request.POST.get('current')

        form = formFilter
        tipo_tarefas = request.POST.get('filtro_tipo')
        estado_tarefa = request.POST.get('filtro_estado')
        txt = request.POST.get('current')

        if estado_tarefa == "Concluida":
            estado = 'Concluida'
        elif estado_tarefa == "naoConcluida":
            estado = 'naoConcluida'
        elif estado_tarefa == "Iniciada":
            estado = 'Iniciada'  
        elif estado_tarefa == "Cancelada":
            estado = 'Cancelada'    

        if txt != "":
            nome = txt.split()
            if estado_tarefa != "":
                tarefas = Tarefa.objects.filter(
                    estado=estado, nome=current,colab=user)
            else:
                tarefas = Tarefa.objects.filter(
                    nome=current)
        elif estado_tarefa == "":#####
            if tipo_tarefas == "Tarefa":
                tarefas = Tarefa.objects.filter(colab=user)
            elif tipo_tarefas == "tarefaAuxiliar":
                tarefas = TarefaAuxiliar.objects.filter(colab=user)
            elif tipo_tarefas == "tarefaAcompanhar":
                tarefas = TarefaAcompanhar.objects.filter(colab=user)
            elif tipo_tarefas == "tarefaOutra":
                tarefas= TarefaOutra.objects.filter(colab=user)
        else:
            if tipo_tarefas == "Tarefa":
                tarefas = Tarefa.objects.filter(
                    estado=estado,colab=user)
            elif tipo_tarefas == "tarefaAuxiliar":
                tarefas = TarefaAuxiliar.objects.filter(
                    estado=estado,colab=user)
            elif tipo_tarefas == "tarefaAcompanhar":
                tarefas = TarefaAcompanhar.objects.filter(
                    estado=estado,colab=user)
            elif tipo_tarefas == "tarefaOutra":
                tarefas = TarefaOutra.objects.filter(
                    estado=estado,colab=user)
    else:
        formFilter = TarefaFiltro()
        current = ""
        tarefas=Tarefa.objects.filter(colab=user).order_by('nome')
        form = formFilter


    paginator= Paginator(tarefas,5)
    page=request.GET.get('page')
    tarefas = paginator.get_page(page)
    return render(request=request, template_name='colaboradores/consultar_tarefas.html', context={"tarefas": tarefas, 'form': form, 'current': current, 'u': u})


# Funcionalidade de conclusao de uma tarefa do colaborador

def concluir_tarefa(request, id): 
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5)


    tarefa = Tarefa.objects.get(id=id)
    tarefa.estado="Concluida"
    tarefa.save()
    msg="Tarefa concluída com sucesso!"
    return render(request=request,
                  template_name="colaboradores/tarefa_concluida.html",
                  context={"msg": msg})


# Funcionalidade de inicio de uma tarefa do colaborador

def iniciar_tarefa(request, id): 
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5)


    tarefa = Tarefa.objects.get(id=id)
    tarefa.estado="Iniciada"
    tarefa.save()
    return redirect('colaboradores:consultar-tarefas')   


# Funcionalidade de cancelamento de uma tarefa do colaborador
def cancelar_tarefa(request, id): 
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5)
    # Envio de notificacao automatica
    views.enviar_notificacao_automatica(request,"cancelarTarefa",id)
    return redirect('notificacoes:notificar',id) 

def validar_cancelamento_tarefa(request, id):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
    try:
        tarefa = Tarefa.objects.get(id=id)
        tarefa.estado="Cancelada"
        tarefa.save()
        views.enviar_notificacao_automatica(request,"confirmarCancelarTarefa",id)
    except:
        return redirect('utilizadores:mensagem',11)    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def rejeitar_cancelamento_tarefa(request, id):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
    try:
        tarefa = Tarefa.objects.get(id=id)    
        views.enviar_notificacao_automatica(request,"rejeitarCancelarTarefa",id)
    except:
        return redirect('utilizadores:mensagem',11)      
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



