from django.shortcuts import render, redirect  
from .forms import AtividadeForm , SessaoForm
from .models import *
from configuracao.models import Horario
from coordenadores.models import Coordenador
from utilizadores.models import Professoruniversitario  
from django.http import HttpResponseRedirect
from datetime import datetime

#-------------Diogo----------------------

def proporatividade(request):
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

def minhasatividades(request):
	return render(request=request,
				template_name="atividades/listaAtividades.html",
                context={"atividades": Atividade.objects.all()})

def alterarAtividade(request,id):
    change_activity= Atividade.objects.get(id=id)
    schedules=Horario.objects.all()
    activity_sessions=Atividadesessao.objects.filter(atividadeid=id)
    espacos=Espaco.objects.all()
    #print(activity_sessions.sessaoid.espacoid.nome)
    changed_form=AtividadeForm(instance=change_activity)
    if request.method == 'POST':
        change_activity.estado='Pendente'
        changed_form=AtividadeForm(request.POST,instance=change_activity)
        if changed_form.is_valid():
            changed_form.save()
            change_activity.dataalteracao = datetime.now()
            change_activity.save()
            return HttpResponseRedirect('/minhasatividades')          
    return render(request=request,
                    template_name='atividades/proporatividade.html',
                    context={'form': changed_form,'schedules':schedules,'activity_sessions':activity_sessions,'espacos':espacos}
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
    