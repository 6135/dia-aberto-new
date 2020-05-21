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

# Funcionalidade de consultar tarefas do colaborador atual, funcionalidades de filtros para a a consulta das tarefas

def consultar_tarefas(request):
        
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        else:
            return redirect('tarefas:mensagem',5)
    else:
        return redirect('tarefas:mensagem',5)  


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
            return redirect('colaboradores:mensagem',5) 
    else:
        return redirect('colaboradores:mensagem',5)


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
            return redirect('colaboradores:mensagem',5) 
    else:
        return redirect('colaboradores:mensagem',5)


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
            return redirect('colaboradores:mensagem',5) 
    else:
        return redirect('colaboradores:mensagem',5)

    tarefa = Tarefa.objects.get(id=id)
    tarefa.estado="Cancelada"
    tarefa.save()
    return redirect('colaboradores:consultar-tarefas') 



# Template de mensagens para mostrar mensagem de erro/sucesso/informação

def mensagem(request, id):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""


    if id == 1:
        user = get_user(request)
        m = "Bem vindo(a) "+user.first_name
        tipo = "info"

    elif id == 2:
        m = "Até á próxima!"
        tipo = "info"

    elif id == 3:
        m = "Registo feito com sucesso!"
        tipo = "sucess"

    elif id == 4:
        m = "É necessário fazer login primeiro"
        tipo = "error"

    elif id == 5:
        m = "Não permitido"
        tipo = "error"
    elif id == 6:
        m = "Senha alterada com sucesso!"
        tipo = "success"    
    elif id == 7:
        m = "Conta apagada com sucesso"
        tipo = "success"   
    elif id == 8:
        m = "Perfil alterado com sucesso"
        tipo = "success" 
    elif id == 9:
        m = "Perfil criado com sucesso"
        tipo = "success"                         
    else:
        return redirect('utilizadores:login')
 
    return render(request=request,
        template_name="colaboradores/mensagem.html", context={'m': m, 'tipo': tipo ,'u': u})