from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
from .models import *
from utilizadores.models import *
from datetime import datetime, timezone,date, time

# Create your views here.

def homepage(request):
	return render(request=request,
				  template_name="configuracao/inicio.html",)

def filter(request, list_diaaberto):
	if request.method == 'POST':
		search_specific = request.POST['searchAno']
		if search_specific != "" and int(search_specific) > 0:
			list_diaaberto = list_diaaberto.filter(ano=search_specific)
		sort_by = request.POST['orderBy']
		if sort_by == "":
			sort_by = 'ano'
		list_diaaberto = list_diaaberto.order_by(sort_by)

		if 'activeDays' in request.POST:
			print('here2')
			today = datetime.now(timezone.utc)
			list_diaaberto.filter(datadiaabertofim__gt=today)
			print(list_diaaberto )
	else:
		list_diaaberto = list_diaaberto.order_by('ano')
		search_specific = ""
	
	
	return {'list_diaaberto': list_diaaberto, 'current': {'specific_year': search_specific}}

def viewDays(request):

	list_diaaberto = Diaaberto.objects.all()	#Obtain all days

	earliest = list_diaaberto.first()	#Obtain some constants
	latest = list_diaaberto.last()
	is_open =(latest.datadiaabertofim > datetime.now(timezone.utc))

	filterRes = filter(request, list_diaaberto)		#Filter/order
	list_diaaberto = filterRes['list_diaaberto']

	current = filterRes['current']

	return render(request=request,
				  template_name='configuracao/listaDiaAberto.html', 
				  context = {'diaabertos': list_diaaberto, 'earliest': (earliest.ano), 'latest': (latest.ano), 'is_open': is_open, 'current': current})

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
		dia_aberto = Diaaberto.objects.get(id=id,administradorutilizadorid=1)
		dia_aberto.delete()
	return redirect('diasAbertos')
