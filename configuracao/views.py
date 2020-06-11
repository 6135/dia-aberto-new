from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from .forms import *
from .models import *
from utilizadores.models import *
from inscricoes.models import Inscricao, Inscricaosessao, Inscricaotransporte
from atividades.models import Tema
from datetime import datetime, timezone,date, time
from atividades.models import Sessao
from django.core.serializers import *
from django.db.models import Count, Q
import random
from _datetime import timedelta
import json
from pip._vendor import requests
from django.core import serializers

# Create your views here.

def user_check(request, user_profile = Administrador):
	if not request.user.is_authenticated:
		return redirect('utilizadores:login')
	elif not user_profile.objects.filter(utilizador_ptr_id = request.user.id).exists():
		return render(request=request,
					template_name='mensagem.html',
					context={
						'tipo':'error',
						'm':'Não tem permissões para aceder a esta pagina!'
					})
	return None

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

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	if request.method == 'POST':
		formFilter = diaAbertoFilterForm(request.POST)
	else:
		formFilter = diaAbertoFilterForm()

	list_diaaberto = Diaaberto.objects.all()	#Obtain all days

	earliest = Diaaberto.objects.all().order_by('ano').first()	#Obtain some constants
	latest = Diaaberto.objects.all().order_by('ano').last()
	current = Diaaberto.objects.filter(ano=datetime.now().year).first()
	is_open=False
	latest_year = 9999
	earliest_year = 0
	if earliest is not None: 
		if current is not None:
			is_open = (current.datadiaabertofim > datetime.now(timezone.utc))
		latest_year = latest.ano
		earliest_year = earliest.ano
	

	filterRes = orderBy(request, list_diaaberto)		#Filter/order
	list_diaaberto = filterRes['list_diaaberto']
	current = filterRes['current']

	list_diaaberto = showBy(request,list_diaaberto)

	return render(request=request,
				  template_name='configuracao/listaDiaAberto.html',
				  context = {'form':formFilter, 'diaabertos': list_diaaberto, 'earliest': earliest_year,
							'latest': latest_year, 'is_open': is_open, 'current': current,
							}
					)

def newDay(request, id=None):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	logged_admin = Administrador.objects.get(utilizador_ptr_id = request.user.id)

	if id is None:
		dia_aberto = Diaaberto(administradorutilizadorid=logged_admin)
	else:
		dia_aberto = Diaaberto.objects.get(id=id,administradorutilizadorid=logged_admin)
		print(dia_aberto.session_times())

	dia_aberto_form = diaAbertoSettingsForm(instance=dia_aberto)

	if request.method == 'POST':
		submitted_data = request.POST.copy()
		dia_aberto_form = diaAbertoSettingsForm(submitted_data, instance=dia_aberto)

		if dia_aberto_form.is_valid():
			dia_aberto_form.save()
			return redirect('configuracao:diasAbertos')

	return render(request=request,
				template_name = 'configuracao/diaAbertoForm.html',
				context = {'form': dia_aberto_form})

def delDay(request, id=None):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	if id is not None:
		dia_aberto = Diaaberto.objects.filter(id=id)
		dia_aberto.delete()
	return redirect('configuracao:diasAbertos')

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

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	form = menusFilterForm(request.POST)
	menus = Menu.objects.all()
	menus = filterMenus(request,menus)
	return render(request=request,
				  template_name='configuracao/listaMenu.html',
				  context = {'menus': menus, 'form': form}
				)

def newMenu(request, id = None):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	PratoFormSet = menuPratoFormset()
	prato_form_set = PratoFormSet(queryset=Prato.objects.none())
	menu_object = Menu()

	if id is not None:
		menu_object = Menu.objects.get(id=id)
		prato_form_set = PratoFormSet(queryset=Prato.objects.filter(menuid=menu_object))
	menu_form = menuForm(instance=menu_object)

	if request.method == 'POST':
		menu_form = menuForm(request.POST,instance=menu_object)
		prato_form_set = PratoFormSet(request.POST)
		if menu_form.is_valid() and prato_form_set.is_valid():
			menu_object = menu_form.save()
			instances = prato_form_set.save(commit=False)

			for instance in instances:
				instance.menuid = menu_object
				instance.save()
			for instance in prato_form_set.deleted_objects:
				instance.delete()
			return redirect('configuracao:verMenus')
	return render(request=request,
				  template_name='configuracao/menuForm.html',
				  context = {'form': menu_form, 'formset': prato_form_set}
				)

def delMenu(request, id = None):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	menu=Menu.objects.get(id=id)
	menu.delete()
	return redirect('configuracao:verMenus')

def menuPratoFormset(extra = 0, minVal = 1):
	formSets = modelformset_factory(model=Prato, exclude = ['id','menuid'],widgets={
			'tipo': Select(attrs={'class': 'input'}),
			'prato': TextInput(attrs={'class': 'input'}),
			'nrpratosdisponiveis': NumberInput(attrs={'class': 'input', 'min':'1','style':'width: 30%'}),
		},labels={
			'nrpratosdisponiveis': '# Pratos'
		}, extra = extra, min_num = minVal, can_delete=True)
	return formSets

def delPrato(request, id):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	prato=Prato.objects.get(id=id)
	menuid=prato.menuid.id
	prato.delete()
	return redirect('configuracao:novoPrato',menuid)

def newPratoRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_tipo': "form-" + str(value-1) + "-tipo",
		'form_prato': "form-" + str(value-1) + "-prato",
		'form_num': "form-" + str(value-1) + "-nrpratosdisponiveis",
		'form_id': 'form-' + str(value-1) + '-id',
	}
	return render(request=request, template_name='configuracao/menuPratoRow.html', context=data)

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

def filtrarTransportes(request, transportes):
	search_specific = None
	if request.method == 'POST':
		search_specific = request.POST.get('searchId')
		if search_specific != '':
			transportes = transportes.filter(transporte__identificador = search_specific)
		if request.POST.get('filter_to') != '':
			transportes = transportes.filter(chegada = request.POST.get('filter_to'))
		if  request.POST.get('filter_from') != '':
			transportes = transportes.filter(origem = request.POST.get('filter_from'))
	return transportes

def verTransportes(request):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	form = transporteFilterForm(request.POST)
	transportes = filtrarTransportes(request = request,transportes = Transportehorario.objects.all())

	return render(request = request,
				  template_name='configuracao/listaTransportes.html',
				  context={'horariosTra': transportes, 'form': form})

def criarTransporte(request, id = None):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	#vars
	transport_by_default = Transporte()
	transport_universitario_default = Transporteuniversitario(transporte=transport_by_default)
	#forms
	HorarioFormSet = transporteHorarioFormset()
	horario_form_set = HorarioFormSet(queryset=Transportehorario.objects.none())
	form_transport = transporteForm()
	form_universitario = transporteUniversitarioForm()

	if id is not None:

		transport_by_default = Transporte.objects.get(id=id)
		transport_universitario_default = Transporteuniversitario(transporte=transport_by_default)
		horario_form_set = HorarioFormSet(queryset=Transportehorario.objects.filter(transporte=transport_by_default))
		form_transport = transporteForm(instance=transport_by_default)
		form_universitario = transporteUniversitarioForm(instance=Transporteuniversitario.objects.get(transporte=transport_by_default))

	if request.method == "POST":
		form_transport = transporteForm(request.POST, instance=transport_by_default)
		form_universitario = transporteUniversitarioForm(request.POST, instance=transport_universitario_default)
		horario_form_set = HorarioFormSet(request.POST)
		if form_transport.is_valid() and form_universitario.is_valid() and horario_form_set.is_valid():

			transport = form_transport.save()
			form_universitario.instance.transporte = transport
			form_universitario.save()
			instances = horario_form_set.save(commit=False)

			for instance in instances:
				instance.transporte = transport
				instance.save()
			for instance in horario_form_set.deleted_objects:
				instance.delete()

			return redirect('configuracao:verTransportes')
		print(form_transport.errors)
		print(form_universitario.errors)
		print(horario_form_set.errors)

	return render(request = request,
				template_name='configuracao/criarTransporte.html',
				context={'form_t': form_transport,
						'form_uni': form_universitario,
						'formset': horario_form_set})

def transporteHorarioFormset(extra = 0, minVal = 1):
	formSets = modelformset_factory(model=Transportehorario, exclude = ['transporte','id'],widgets={
			'origem': Select(attrs={'class': 'input'}),
			'chegada': Select(attrs={'class': 'input'}),
			'horaPartida': CustomTimeWidget(attrs={'class': 'input'}),
			'horaChegada': CustomTimeWidget(attrs={'class': 'input'}),
		}, extra = extra, min_num = minVal, can_delete=True)
	return formSets

def newHorarioRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_origem': "form-" + str(value-1) + "-origem",
		'form_chegada': "form-" + str(value-1) + "-chegada",
		'form_horaPartida': "form-" + str(value-1) + "-horaPartida",
		'form_horaChegada': "form-" + str(value-1) + "-horaChegada",
		'form_id': 'form-' + str(value-1) + '-id',
	}
	return render(request=request, template_name='configuracao/transporteHorarioEmptyRow.html', context=data)


def eliminarTransporte(request, id):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	Transportehorario.objects.get(id=id).delete()
	return redirect('configuracao:verTransportes')


def atribuirTransporte(request, id):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	class ChegadaPartida:
		def __init__(self, id,nparticipantes,local,horario, check):
			self.id=id
			self.nparticipantes=nparticipantes
			self.local= local
			self.horario=horario
			self.check=check

	transportehorario = Transportehorario.objects.get(id=id)
	inscricoesindisponiveis= []
	inscricaotransporte= Inscricaotransporte.objects.filter(transporte=transportehorario.id)
	ocupadas=0
	for ocp in inscricaotransporte:
		ocupadas+=ocp.npassageiros
	print(ocupadas)
	transportevagas= transportehorario.transporte.transporteuniversitario.capacidade - ocupadas
	inscricoestotais = Inscricao.objects.filter(nalunos__lte=transportevagas)
	dadoschepart= []
	inscricoes= []

	for t in inscricaotransporte:
		inscricoesindisponiveis.append(t.inscricao)
	
	for inscricao in inscricoestotais:
		if inscricao not in inscricoesindisponiveis:
					inscricoes.append(inscricao)
		
	for inscricao in inscricoes:
		isessaochegada=Inscricaosessao.objects.filter(inscricao=inscricao.id).order_by('sessao__horarioid__inicio').first()
		if isessaochegada.sessao.dia == transportehorario.transporte.dia:
			if transportehorario.origem == "Gambelas" or transportehorario.origem == "Penha":
				isessaopartida=Inscricaosessao.objects.filter(inscricao=inscricao.id).order_by('-sessao__horarioid__inicio').first() # ultima sessao da inscricao
				isessaopartidalocal= isessaopartida.sessao.atividadeid.espacoid.edificio.campus.nome	# campus ultima sessao da inscricao
				isessaopartidahorario= isessaopartida.sessao.horarioid.fim #horario de fim da ultima sessao
				horapartida= (transportehorario.horaPartida.hour*60 + transportehorario.horaPartida.minute) - (isessaopartidahorario.hour*60 + isessaopartidahorario.minute) # diferença entre horario transporte e da ultima sessao
				if isessaopartidalocal == transportehorario.origem  and horapartida <=60:
					chepart= ChegadaPartida(inscricao.id, inscricao.nalunos,inscricao.localchegada, isessaopartidahorario, True)
			else:
				isessaochegadalocal= isessaochegada.sessao.atividadeid.espacoid.edificio.campus.nome
				horachegada= (transportehorario.horaChegada.hour*60 + transportehorario.horaChegada.minute )- (inscricao.horariochegada.hour*60 + inscricao.horariochegada.minute)
				if isessaochegadalocal == transportehorario.chegada and horachegada <=60:
					chepart= ChegadaPartida(inscricao.id,inscricao.nalunos,inscricao.localchegada,inscricao.horariochegada, False)

			dadoschepart.append(chepart)




	print(inscricoes)
	if request.method == "POST":
		gruposid=request.POST["gruposid"]
		if "new" in request.POST:
			grupo= Inscricao.objects.get(id=gruposid)
			new_inscricaotransporte= Inscricaotransporte(transporte=transportehorario, npassageiros=grupo.nalunos, inscricao= grupo)
			new_inscricaotransporte.save()
			return redirect('configuracao:atribuirTransporte', id)

	return render(request = request,
				  template_name='configuracao/atribuirTransporte.html',
				  context={'transporte': transportehorario,  "inscricoestransporte": inscricaotransporte, "vagas": transportevagas, 'chegadapartida': dadoschepart})

def eliminarAtribuicao(request, id):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	transportehorario=Inscricaotransporte.objects.get(id=id).transporte.id
	print(transportehorario)
	Inscricaotransporte.objects.get(id=id).delete()
	return redirect('configuracao:atribuirTransporte', transportehorario)

def verEdificios(request):
	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	edificios = Edificio.objects.all()

	return render(request=request,
				template_name='configuracao/listaEdificios.html',
				context={'edificios': edificios})

def configurarEdificio(request, id = None):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	espacoFormSet = modelformset_factory(model=Espaco, form=EspacoForm,extra=0, min_num = 1, can_delete=True)
	formSet = espacoFormSet(queryset=Espaco.objects.none())
	edificio = Edificio()

	if id is not None:
		edificio = Edificio.objects.get(id=id)
		formSet = espacoFormSet(queryset=Espaco.objects.filter(edificio=edificio))
	edificioForm = EdificioForm(instance=edificio)


	if request.method == 'POST':
		edificioForm = EdificioForm(data=request.POST,instance=edificio)
		formSet = espacoFormSet(request.POST)
		if edificioForm.is_valid() and formSet.is_valid():
			print("valid")
			edificio = edificioForm.save()

			instances = formSet.save(commit=False)

			for instance in instances:
				instance.edificio=edificio
				instance.save()

			for instance in formSet.deleted_objects:
				instance.delete()

			return redirect('configuracao:verEdificios')

	return	render(request=request,
				template_name='configuracao/criarEdificio.html',
				context={'form':edificioForm,
						'formset':formSet})

def newEspacoRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_nome': "form-" + str(value-1) + "-nome",
		'form_espaco': "form-" + str(value-1) + "-espaco",
		'form_descricao': "form-" + str(value-1) + "-descricao",
		'form_id': 'form-' + str(value-1) + '-id',
	}
	return render(request=request, template_name='configuracao/edificioEspacoRow.html', context=data)

def eliminarEdificio(request,id):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	Edificio.objects.get(id=id).delete()
	return redirect('configuracao:verEdificios')

def verTemas(request):
	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	temas = Tema.objects.all()

	return render(request=request,
				template_name='configuracao/listaTemas.html',
				context={'temas': temas})

def configurarTema(request, id = None):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	tema = Tema()

	if id is not None:
		tema = Tema.objects.get(id=id)
	temaForm = TemaForm(instance=tema)


	if request.method == 'POST':
		temaForm = TemaForm(data=request.POST,instance=tema)
		if temaForm.is_valid():
			tema = temaForm.save()
			return redirect('configuracao:verTemas')

	return	render(request=request,
				template_name='configuracao/criarTema.html',
				context={'form':temaForm})

def eliminarTema(request,id):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	Tema.objects.get(id=id).delete()
	return redirect('configuracao:verTemas')


def verUOs(request):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	uos = Unidadeorganica.objects.all()

	return render(request=request,
				template_name='configuracao/listaUO.html',
				context={'UOs': uos})

def configurarUO(request, id = None):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	if(id is None):
		pass
	
	if(request.method == 'POST'):
		pass

	if(id is None):
		pass
	else: 
		pass
	
	pass

def eliminarUO(request, id):

	user_check_var = user_check(request=request, user_profile=Administrador)
	if user_check_var is not None: return user_check_var

	Unidadeorganica.objects.get(id=id).delete()
	return redirect('configuracao:veruos')