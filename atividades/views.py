from django.shortcuts import render, redirect  
from .forms import AtividadeForm , SessaoForm, EspacoForm 
from .models import Atividade, Espaco, Sessao, Horario
from coordenadores.models import Coordenador
from utilizadores.models import Professoruniversitario  
from atividades.forms import HorarioForm
from configuracao.models import Diaaberto
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
    
    if request.method == 'POST':
        change_activity.estado='Pendente'
        changed_form=AtividadeForm(request.POST,instance=change_activity)
        if changed_form.is_valid():
            changed_form.save() 
            return HttpResponseRedirect('/thanks/')
        else:
            return HttpResponseRedirect('/didntwork/')
    else:
        return render(request=request,
                    template_name='atividades/proporatividade.html',
                    context={'atividade': change_activity}
                    )
#-----------------EndDiogo------------------


#-----------------------David--------------------
def inseriratividade(request):  
    if request.method == "POST":
        form_Sessao= SessaoForm(request.POST)
        form_horario= HorarioForm(request.POST)
        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),
                             professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),
                             estado = "Pendente", diaabertoid = Diaaberto.objects.all().order_by('-id').first())
        formAtividade = AtividadeForm(request.POST, instance=new_form) 
        if formAtividade.is_valid() and form_Sessao.is_valid() and form_horario.is_valid():
            new_form.save()
            
            sessao = form_Sessao.save(commit= False)
            sessao.vagas= sessao.participantesmaximo
            sessao.ninscritos= 0
            sessao.espacoid= Espaco.objects.get(id=1)
            sessao.horarioid= Horario.objects.get(id=1)
            sessao.save()
            return HttpResponseRedirect('/thanks/')
        else:
            return render(request, 'atividades/inseriratividade.html',{'atividade': formAtividade , 'sessao': form_Sessao, 'horario':Horario.objects.all(), 'horat': form_horario})
    else:  
        formAtividade = AtividadeForm()
        form_Sessao= SessaoForm()
        form_horario= HorarioForm()  
    return render(request,'atividades/inseriratividade.html',{'atividade': formAtividade,'sessao': form_Sessao,'horario':Horario.objects.all(), 'horat': form_horario})  
#---------------------End David
    