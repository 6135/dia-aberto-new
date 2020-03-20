from django.shortcuts import render, redirect  
from .forms import AtividadeForm , SessaoForm, EspacoForm 
from .models import Atividade, Espaco, Sessao
from coordenadores.models import Coordenador
from utilizadores.models import Professoruniversitario  
from django.http import HttpResponseRedirect

#-------------Diogo---------------------

def proporatividade(request):
	return render(request=request,
				  template_name="atividades/proporatividade.html",)

def minhasatividades(request):
	return render(request=request,
				template_name="atividades/listaAtividades.html",)
#-----------------EndDiogo------------------


#-----------------------David--------------------
def inseriratividade(request):  
    if request.method == "POST":
    	formEspaco = EspacoForm(request.POST)
        new_formAtividade = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),estado = "Pendente")
        formAtividade = AtividadeForm(request.POST, instance=new_formAtividade) 
        if formAtividade.is_valid():
            new_formAtividade.save()
    else:  
        formAtividade = AtividadeForm()
        #formSessao = SessaoForm()   
    return render(request,'atividades/inseriratividade.html',{'form_Atividade': formAtividade, 'form_Espaco': formEspaco})  
#---------------------End David
    