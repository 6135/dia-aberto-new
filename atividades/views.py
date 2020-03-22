from django.shortcuts import render, redirect  
from .forms import AtividadeForm , SessaoForm 
from .models import Atividade, Sessao, Coordenador, Professoruniversitario  
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
        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),
                             professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),
                             estado = "Pendente")
        formAtividade = AtividadeForm(request.POST, instance=new_form) 
        if formAtividade.is_valid():
            new_form.save()
            return HttpResponseRedirect('/thanks/')
        else:
            return render(request, 'inseriratividade.html',{'form_Atividade': formAtividade, 'log': True})
    else:  
        formAtividade = AtividadeForm()
        #formSessao = SessaoForm()   
    return render(request,'inseriratividade.html',{'form_Atividade': formAtividade})  
#---------------------End David
    