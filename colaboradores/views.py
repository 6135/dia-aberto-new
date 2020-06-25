from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from utilizadores.models import *
from configuracao.models import *
from coordenadores.models import *
from notificacoes.models import *
from django.shortcuts import redirect
from .forms import *
from .tables import TarefasTable
from .filters import TarefasFilter
from django.contrib.auth import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from django.core.paginator import Paginator

from notificacoes import views
from django.utils.datetime_safe import date
from utilizadores.views import user_check


class consultar_tarefas(SingleTableMixin, FilterView):
    ''' Funcionalidade de consultar tarefas do colaborador atual, funcionalidades de filtros para a a consulta das tarefas '''
    template_name = 'colaboradores/consultar_tarefas.html'
    table_class = TarefasTable
    filterset_class = TarefasFilter
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(
            request=request, user_profile=[Colaborador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user_check_var = user_check(
            request=self.request, user_profile=[Colaborador])
        return Tarefa.objects.filter(colab=self.request.user)
    

def consultar_tarefas_old(request):
        
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
        elif estado_tarefa == "":
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
    return render(request=request, template_name='colaboradores/consultar_tarefas_old.html', context={"tarefas": tarefas, 'form': form, 'current': current, 'u': u})



def concluir_tarefa(request, id): 
    ''' Funcionalidade de conclusão de uma tarefa do colaborador '''
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



def iniciar_tarefa(request, id): 
    ''' Funcionalidade de inicio de uma tarefa do colaborador '''
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



def cancelar_tarefa(request, id):
    ''' Funcionalidade de cancelamento de uma tarefa do colaborador ''' 
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5)
    # Envio de notificação automática
    views.enviar_notificacao_automatica(request,"cancelarTarefa",id) #Envio de notificação automática !!!!
    tarefa = Tarefa.objects.get(id=id)
    nome = tarefa.coord.first_name+" "+tarefa.coord.last_name
    msg = "A enviar pedido de cancelamento de tarefa a "+nome
    return render(request=request,
                  template_name="colaboradores/enviar_notificacao_informativa.html",
                  context={"msg": msg})


def validar_cancelamento_tarefa(request, id_notificacao):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
    try:
        notificacao = Notificacao.objects.get(id=id_notificacao)
        notificacao.deleted = True
        id_tarefa = notificacao.action_object.id
        notificacao.save()
        tarefa = Tarefa.objects.get(id=id_tarefa)
        tarefa.estado="Cancelada"
        tarefa.save()
        views.enviar_notificacao_automatica(request,"confirmarCancelarTarefa",id_tarefa)
    except:
        return redirect('utilizadores:mensagem',11)    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def rejeitar_cancelamento_tarefa(request, id_notificacao):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
    try:
        notificacao = Notificacao.objects.get(id=id_notificacao)
        notificacao.deleted = True
        id_tarefa = notificacao.action_object.id
        notificacao.save() 
        views.enviar_notificacao_automatica(request,"rejeitarCancelarTarefa",id_tarefa)
    except:
        return redirect('utilizadores:mensagem',11)      
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



