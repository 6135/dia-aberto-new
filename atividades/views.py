from django.shortcuts import render, redirect  
from .forms import AtividadeForm , MateriaisForm
from .models import *
from configuracao.models import Horario
from .models import Atividade, Espaco, Sessao, Atividadesessao, Tema
from coordenadores.models import Coordenador
from utilizadores.models import Professoruniversitario  
from configuracao.models import Diaaberto, Horario
from django.http import HttpResponseRedirect
from datetime import datetime



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
                    context={'atividade': change_activity,'form': changed_form,'schedules':schedules,'activity_sessions':activity_sessions,'espacos':espacos}
                    )
#-----------------EndDiogo------------------


#-----------------------David--------------------
def inseriratividade(request):  
    if request.method == "POST":
        form_Materiais= MateriaisForm(request.POST)
        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),
                             professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),
                             estado = "Pendente", diaabertoid = Diaaberto.objects.all().order_by('-id').first(),espacoid= Espaco.objects.get(id=request.POST['idespaco']),tema=Tema.objects.get(id=request.POST['idtema']))
        formAtividade = AtividadeForm(request.POST, instance=new_form)
        
        if formAtividade.is_valid() and  form_Materiais.is_valid():
            new_form.save()  
            materiais = form_Materiais.save(commit= False)
            materiais.atividadeid = Atividade.objects.all().order_by('-id').first()
            materiais.save()
            idAtividade= Atividade.objects.all().order_by('-id').first()
            return redirect('inserirSessao', idAtividade.id)
        else:
            return render(request, 'atividades/proporatividade.html',{'form': formAtividade ,'horario':  Horario.objects.all(), 'espaco': Espaco.objects.all(), 'mat': form_Materiais, 'theme':Tema.objects.all()})
    else:  
        formAtividade = AtividadeForm()
        form_Materiais= MateriaisForm() 
    return render(request,'atividades/proporatividade.html',{'form': formAtividade,'horario':  Horario.objects.all(), 'espaco': Espaco.objects.all,'mat': form_Materiais,'theme':Tema.objects.all()})  



def inserirsessao(request,id):
    disp= []
    hor_indis= Atividadesessao.objects.all().filter(atividadeid=id)
    indis= []
    for sessao in hor_indis:
        indis.append(sessao.sessaoid.horarioid)
    for t in Horario.objects.all():
        if  t not in indis:
            disp.append(t) 
    print(disp)             
    if request.method == "POST":
            new_Sessao= Sessao(vagas=Atividade.objects.get(id= id).participantesmaximo,ninscritos=0 ,horarioid=Horario.objects.get(id=request.POST['idhorario']))
            new_Sessao.save()
            new_as = Atividadesessao(atividadeid = Atividade.objects.get(id=id), sessaoid= Sessao.objects.all().order_by('-id').first())
            new_as.save()
            
            if 'save' in request.POST:
                return HttpResponseRedirect('/thanks/')
            elif 'new' in request.POST:
                return redirect('inserirSessao', id)
    return render(request,'atividades/inserirsessao.html',{'horario': disp })  






#---------------------End David
    