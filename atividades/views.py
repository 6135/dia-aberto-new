from django.shortcuts import render, redirect
from .models import Atividade

#-------------Diogo---------------------

def proporatividade(request):
	return render(request=request,
				  template_name="atividades/proporatividade.html",)

def minhasatividades(request):
	return render(request=request,
				  template_name="atividades/listaAtividades.html",)
#-----------------EndDiogo------------------