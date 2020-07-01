from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from utilizadores.models import *
from configuracao.models import *
from coordenadores.models import *
from colaboradores.models import *
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
from django.forms.models import modelformset_factory

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
		return Tarefa.objects.filter(colab=self.request.user)



def minha_disponibilidade(request): 
	''' Página onde o colaborador seleciona a disponibilidade para desempenhar tarefas escolhendo desta forma o(s) horário(s) que lhe dá mais jeito '''
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = Colaborador.objects.get(id=user.id)      
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)

	HorarioFormSet = preferenciaHorarioFormset()
	horario_form_set = HorarioFormSet(queryset=ColaboradorHorario.objects.none())

	if request.method == "POST":
		horario_form_set = HorarioFormSet(request.POST)
		values = PreferenciaTarefasForm(request.POST)	
		if form_transport.is_valid() and form_universitario.is_valid() and horario_form_set.is_valid():

			instances = horario_form_set.save(commit=False)

			for instance in instances:
				instance.colab = u.id
				instance.save()
			for instance in horario_form_set.deleted_objects:
				instance.delete()
			
			if values == "tarefaAcompanhar":
				Preferencia(colab = u.id, tipoTarefa = "tarefaAcompanhar")
			if values == "tarefaAuxiliar":
				Preferencia(colab = u.id, tipoTarefa = "tarefaAuxiliar")
			if values == "tarefaOutra":
				Preferencia(colab = u.id, tipoTarefa = "tarefaOutra") 

			return redirect('colaboradores:concluir-disponibilidade')
	else:
		form_preferencia_tarefas = PreferenciaTarefasForm()	
	return render(request = request,
				template_name='colaboradores/minha_disponibilidade.html',
				context={'form_preferencia_tarefas': form_preferencia_tarefas,
				'horario_form_set': horario_form_set,})


def preferenciaHorarioFormset(extra = 0, minVal = 1):
	formSets = modelformset_factory(model=ColaboradorHorario, exclude = ['colab','id'],widgets={
			'dia': Select(attrs={'class': 'input'}),
			'inicio': CustomTimeWidget(attrs={'class': 'input'}),
			'fim': CustomTimeWidget(attrs={'class': 'input'}),
		}, extra = extra, min_num = minVal, can_delete=True)
	return formSets

def newHorarioRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_dia': "form-" + str(value-1) + "-dia",
		'form_inicio': "form-" + str(value-1) + "-inicio",
		'form_fim': "form-" + str(value-1) + "-fim",
		'form_id': 'form-' + str(value-1) + '-id',
		'dias' : Diaaberto.current().days_as_array() 
	}
	return render(request=request, template_name='colaboradores/preferencia_horario.html', context=data)




def concluir_disponibilidade(request):
	''' Página que é mostrada ao colaborador quando altera a sua disponibilidade na plataforma '''
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = "Colaborador"       
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)

	return render(request=request,
				  template_name="colaboradores/concluir_disponibilidade.html")



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
		notificacao.save()
		id_tarefa = notificacao.action_object.id
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
		notificacao.save() 
		id_tarefa = notificacao.action_object.id
		views.enviar_notificacao_automatica(request,"rejeitarCancelarTarefa",id_tarefa)
	except:
		return redirect('utilizadores:mensagem',11)      
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



