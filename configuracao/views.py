from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
from .models import *
from utilizadores.models import *
from datetime import datetime, timezone,date, time
from atividades.models import Espaco

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
	is_open =(latest.datadiaabertofim > datetime.now(timezone.utc))

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
