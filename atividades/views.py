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
    	#formEspaco = EspacoForm(request.POST)
        CoorId= Coordenador.objects.get(utilizadorid=1)
        ProfId= Professoruniversitario.objects.get(utilizadorid=2)
        new_formAtividade = Atividade(coordenadorutilizadorid = CoorId,
        professoruniversitarioutilizadorid = ProfId,
        estado = "Pendente")
        formAtividade = AtividadeForm(request.POST, instance=new_formAtividade) 
        if formAtividade.is_valid() and formEspaco.is_valid():
            new_formAtividade.save()
            formEspaco.save
    else:  
        formAtividade = AtividadeForm()
        formEspaco = EspacoForm() 
    return render(request,'atividades/inseriratividade.html',{'form_Atividade': formAtividade, 'form_Espaco': formEspaco})  
#---------------------End David-------
    