from django.shortcuts import render, redirect
from .models import Atividade

#-------------Diogo---------------------

def proporatividade(request):
	return render(request=request,
				  template_name="proporatividade.html",)

def minhasatividades(request):
	return render(request=request,
				  template_name="listaAtividades.html",)
#-----------------EndDiogo------------------