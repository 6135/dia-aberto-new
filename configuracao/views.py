from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from .forms import *
from .models import *
from utilizadores.models import *
from datetime import datetime, timezone,date, time
from atividades.models import Espaco
from django.core import serializers
from django.core.serializers import json
from django.db.models import Q
import random
from _datetime import timedelta

# Create your views here.

def homepage(request):
	return render(request=request,
				  template_name="configuracao/inicio.html",)

def orderBy(request, list_diaaberto):
	if request.method == 'POST':
		search_specific = request.POST['searchAno']
		if search_specific != "" and int(search_specific) > 0:
			list_diaaberto = list_diaaberto.filter(ano=search_specific)
		sort_by = request.POST['orderBy']
		if sort_by == "":
			sort_by = '-ano'
		list_diaaberto = list_diaaberto.order_by(sort_by)

	else:
		list_diaaberto = list_diaaberto.order_by('-ano')
		search_specific = ""
	
	return {'list_diaaberto': list_diaaberto, 
			'current': {'specific_year': search_specific,}
			}

def showBy(request, list_diaaberto):
	if request.method == 'POST':
		today = datetime.now(timezone.utc)
		if request.POST['showBy'] == '1':
			list_diaaberto = list_diaaberto.filter(datadiaabertofim__gte=today)
		elif request.POST['showBy'] == '2':
			list_diaaberto = list_diaaberto.filter(dataporpostaatividadesfim__gte=today)
		elif request.POST['showBy'] == '3':
			list_diaaberto = list_diaaberto.filter(datainscricaoatividadesfim__gte=today)
	return list_diaaberto

def viewDays(request):

	if request.method == 'POST':
		formFilter = diaAbertoFilterForm(request.POST)
	else:
		formFilter = diaAbertoFilterForm()

	list_diaaberto = Diaaberto.objects.all()	#Obtain all days

	earliest = Diaaberto.objects.all().order_by('ano').first()	#Obtain some constants
	latest = Diaaberto.objects.all().order_by('ano').last()
	current = Diaaberto.objects.get(ano=datetime.now().year)
	is_open =(current.datadiaabertofim > datetime.now(timezone.utc))

	filterRes = orderBy(request, list_diaaberto)		#Filter/order
	list_diaaberto = filterRes['list_diaaberto']
	current = filterRes['current']

	list_diaaberto = showBy(request,list_diaaberto)

	return render(request=request,
				  template_name='configuracao/listaDiaAberto.html', 
				  context = {'form':formFilter, 'diaabertos': list_diaaberto, 'earliest': (earliest.ano), 
							'latest': (latest.ano), 'is_open': is_open, 'current': current,
							}
					)

def newDay(request, id=None):

	if id is None:
		dia_aberto = Diaaberto(administradorutilizadorid=Administrador.objects.get(id='1'))
	else:
		dia_aberto = Diaaberto.objects.get(id=id,administradorutilizadorid=1)
		
	dia_aberto_form = diaAbertoSettingsForm(instance=dia_aberto)

	if request.method == 'POST':
		submitted_data = request.POST.copy()
		dia_aberto_form = diaAbertoSettingsForm(submitted_data, instance=dia_aberto)

		if dia_aberto_form.is_valid():
			dia_aberto_form.save()
			return redirect('diasAbertos')

	return render(request=request,
				template_name = 'configuracao/diaAbertoForm.html',
				context = {'form': dia_aberto_form})

def delDay(request, id=None):

	if id is not None:
		dia_aberto = Diaaberto.objects.filter(id=id,administradorutilizadorid=1)
		dia_aberto.delete()
	return redirect('diasAbertos')

def view_days_as_json(request): 
	dias = Edificio.objects.all()
	dias_as_json = serializers.serialize('json',list(dias))
	return render(request=request,
				  template_name='configuracao/blank.html', 
				  context = {'dias_as_json': dias_as_json}
				)

def filterMenus(request, menus):
	if request.method == 'POST':
		search_specific = request.POST['searchAno']
		if search_specific != "" and int(search_specific) > 0:
			menus = menus.filter(diaaberto = Diaaberto.objects.get(ano=search_specific))
		filters=['','','']
		if request.POST.get('penha'):
			filters[0]='Penha'
		if  request.POST.get('gambelas'):
			filters[1]='Gambelas'
		if  request.POST.get('portimao'):
			filters[2]='Portimao'			
		if request.POST.get('portimao') or request.POST.get('gambelas') or request.POST.get('penha'):
			menus = menus.filter(Q(campus=Campus.objects.filter(nome=filters[0]).first()) 
						| Q(campus=Campus.objects.filter(nome=filters[1]).first())
						| Q(campus=Campus.objects.filter(nome=filters[2]).first()))
	return menus


def viewMenus(request):
	form = menusFilterForm(request.POST)
	menus = Menu.objects.all()
	menus = filterMenus(request,menus)
	return render(request=request,
				  template_name='configuracao/listaMenu.html',
				  context = {'menus': menus, 'form': form}
				)

def newMenu(request, id = None):
	menu_object = Menu()
	if id is not None:
		menu_object = Menu.objects.get(id=id)
	menu_form = menuForm(instance=menu_object)

	if request.method == 'POST':
		menu_form = menuForm(request.POST,instance=menu_object)
		if menu_form.is_valid():
			menu_form_object = menu_form.save()
			return redirect('novoPrato', menu_form_object.id)

	return render(request=request,
				  template_name='configuracao/menuForm.html',
				  context = {'form': menu_form}
				)

def delMenu(request, id = None):
	menu=Menu.objects.get(id=id)
	menu.delete()
	return redirect('verMenus')


def newPrato(request, id):
	pratos = Prato.objects.filter(menuid=Menu.objects.get(id=id))
	has_one = pratos.count() > 0
	prato_object = Prato(menuid=Menu.objects.get(id=id))
	prato_form=pratosForm(instance=prato_object)
	if request.method == 'POST':
		prato_form=pratosForm(request.POST,instance=prato_object)
		if prato_form.is_valid():
			prato_form.save()
			if 'save' in request.POST:
				return redirect('verMenus')
			else:
				return redirect('novoPrato',id)
	return render(request=request,
				  template_name='configuracao/pratoForm.html',
				  context = {'form': prato_form, 
				  			'pratos': pratos, 
							'has_one': has_one,
							}
				)

def delPrato(request, id):
	prato=Prato.objects.get(id=id)
	menuid=prato.menuid.id
	prato.delete()
	return redirect('novoPrato',menuid)

	
def getDias(request):
	options = []
	default = {
		'key': '',
		'value': 'Escolha um Dia',
	}
	if request.POST['diaaberto_id'] != '':
		if 'default' in request.POST and request.POST['default'] != 'None':
			if request.POST['typeForm'] == 'menu':
				default = { 	
					'key': str(Menu.objects.get(id=request.POST['default']).dia),
					'value': str(Menu.objects.get(id=request.POST['default']).dia),
				}
			if request.POST['typeForm'] == 'transporte':
				default = { 	
					'key': str(Transporte.objects.get(id=request.POST['default']).dia),
					'value': str(Transporte.objects.get(id=request.POST['default']).dia),
				}
		diaaberto = Diaaberto.objects.get(id=request.POST['diaaberto_id'])
		data_inicio = diaaberto.datadiaabertoinicio
		data_fim = diaaberto.datadiaabertofim
		total_dias= data_fim-data_inicio+timedelta(days=1)
		options = diaaberto.days_as_dict()
	return render(request = request,
				  template_name='configuracao/dropdown.html',
				  context={'options':options, 'default': default}
				)
				
#def sourceView(request):
#	return redirect('https://github.com/6135/dia-aberto')

def verTransportes(request):
	form = []
	transporte = Transportehorario.objects.all()
	return render(request = request,
				  template_name='configuracao/listaTransportes.html',
				  context={'form': form, 'horariosTra': transporte})

def criarTransporte(request, id = None):

	HorarioFormSet = transporteHorarioFormset()
	horario_form_set = HorarioFormSet(queryset=Transportehorario.objects.none())
	form_transport = transporteForm()
	form_universitario = transporteUniversitarioForm()

	if id is not None:
		transport_by_default = Transporte.objects.get(id=id)
		horario_form_set = HorarioFormSet(queryset=Transportehorario.objects.filter(transporte=transport_by_default))
		form_transport = transporteForm(instance=transport_by_default)
		form_universitario = transporteUniversitarioForm(Transporteuniversitario(transporte=transport_by_default))

	if request.method == "POST":
		form_transport = transporteForm(request.POST)
		form_universitario = transporteUniversitarioForm(request.POST)
		horario_form_set = HorarioFormSet(request.POST)
		if form_transport.is_valid() and form_universitario.is_valid() and horario_form_set.is_valid():

			transport = form_transport.save()
			form_universitario.instance.transporte = transport
			form_universitario.save()
			instances = horario_form_set.save(commit=False)

			for instance in instances:
				
				instance.transporte = transport
				print(instance)
				instance.save()

			return redirect('verTransportes')

	return render(request = request,
				template_name='configuracao/criarTransporte.html',
				context={'form_t': form_transport,
						'form_uni': form_universitario,
						'formset': horario_form_set})

def transporteHorarioFormset(extra = 0, minVal = 1):
	formSets = modelformset_factory(model=Transportehorario, exclude = ['transporte','id','dia'],widgets={
            'origem': TextInput(attrs={'class': 'input'},),
            'chegada': TextInput(attrs={'class': 'input'}),
            'horaPartida': CustomTimeWidget(attrs={'class': 'input'}),
            'horaChegada': CustomTimeWidget(attrs={'class': 'input'}),
        }, extra = extra, min_num = minVal)
	return formSets

def newHorarioRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_origem': "form-" + str(value-1) + "-origem",
		'form_chegada': "form-" + str(value-1) + "-chegada",
		'form_horaPartida': "form-" + str(value-1) + "-horaPartida",
		'form_horaChegada': "form-" + str(value-1) + "-horaChegada",
	}
	return render(request=request, template_name='configuracao/transporteHorarioEmptyRow.html', context=data)


def atribuirtransporte(request, id):
	return render(request= request, template_name='configuracao/atribuirtransporte.html')