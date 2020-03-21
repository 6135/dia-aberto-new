from django.shortcuts import render, redirect  
from .forms import AtividadeForm , SessaoForm, EspacoForm 
from .models import Atividade, Espaco, Sessao
from coordenadores.models import Coordenador
from utilizadores.models import Professoruniversitario  
from django.http import HttpResponseRedirect

#-------------Diogo----------------------

def proporatividade(request):
	return render(request=request,
				  template_name="atividades/proporatividade.html",)

def minhasatividades(request):
	return render(request=request,
				template_name="atividades/listaAtividades.html",
                context={"atividades": Atividade.objects.all()})

def alterarAtividade(request,id):
    change_activity= Atividade.objects.get(id=id)
    tipos=Atividade.objects.values('tipo')
    print(tipos)
    if request.method == 'POST':
        print(change_activity)
       # formAtividade = AtividadeForm(request.POST, instance=change_activity)
        Atividade.objects
        return HttpResponseRedirect('/thanks/')
    else:
        return render(request=request,
                    template_name='atividades/proporatividade.html',
                    context={'atividade': change_activity}
                    )
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
            return render(request, 'atividades/proporatividade.html',{'atividade': formAtividade})
    else:  
        formAtividade = AtividadeForm()
        #formSessao = SessaoForm()   
    return render(request,'atividades/proporatividade.html',{'atividade': formAtividade})  
#---------------------End David
    