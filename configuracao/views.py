from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .models import *
from django.utils.dateparse import parse_datetime

# Create your views here.

def homepage(request):
	return render(request=request,
				  template_name="configuracao/inicio.html",)

def editdates(request):
	dia_aberto = Diaaberto.objects.get(id=1,administradorutilizadorid=1)
	dia_aberto_form = diaAbertoSettingsForm(instance=dia_aberto)
	print(dia_aberto.datadiaabertoinicio)
	if request.method == 'POST':
		submitted_data = request.POST.copy()

		str_unparsed = submitted_data.__getitem__('datadiaabertoinicio')
		print(parse_datetime(str_unparsed))
		dia_aberto_form = diaAbertoSettingsForm(submitted_data, instance=dia_aberto)

		if dia_aberto_form.is_valid():
			dia_aberto_form.save()

	return render(request=request,
				template_name = 'configuracao/editardatas.html',
				context = {'form': dia_aberto_form})