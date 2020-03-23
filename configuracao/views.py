from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
from .models import *
from utilizadores.models import *
from datetime import datetime

# Create your views here.

def homepage(request):
	return render(request=request,
				  template_name="configuracao/inicio.html",)

def viewDays(request):
	list_diaaberto = Diaaberto.objects.all()
	return render(request=request,
				  template_name='configuracao/listaDiaAberto.html', 
				  context = {'diaabertos': list_diaaberto})

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