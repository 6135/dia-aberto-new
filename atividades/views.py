from django.shortcuts import render, redirect  
from .forms import AtividadeForm , SessaoForm
from .models import *
from configuracao.models import Horario
from .models import Atividade, Espaco, Sessao, Atividadesessao
from coordenadores.models import Coordenador
from utilizadores.models import Professoruniversitario  
from configuracao.models import Diaaberto, Horario
from django.http import HttpResponseRedirect
from datetime import datetime
from atividades.forms import MateriaisForm


#-------------Diogo----------------------
def minhasatividades(request):
	return render(request=request,
				template_name="atividades/listaAtividades.html",
                context={"atividades": Atividade.objects.all()})

def alterarAtividade(request,id):
    #------atividade a alterar----
    activity= Atividade.objects.get(id=id)
    changed_form=AtividadeForm(instance=activity)
    #-----------------------------
    #------sessao da atividade----
    activity_sessions=Atividadesessao.objects.get(atividadeid=id)  
    session=activity_sessions.sessaoid
    changed_session=SessaoForm(instance=session)
    #-----------------------------
    #------horarios&espaços-------
    schedules=Horario.objects.all()
    espacos=Espaco.objects.all()
    #-----------------------------
    if request.method == 'POST':
        activity.estado='Pendente'#apos alteraçao a atividade volta a estado pendente
        changed_activity=AtividadeForm(request.POST,instance=activity)
        changed_session=SessaoForm(request.POST,instance=session)
        if changed_form.is_valid() and changed_session.is_valid():
            changed_form.save()#guardar alteraçoes a sessoes da atividade
            change_session.save()#guardar alteraçoes a atividade
            change_activity.dataalteracao = datetime.now()#data de alteraçao da atividade
            change_activity.save()#guardar a data de alteraçao da atividade           
            return HttpResponseRedirect('/minhasatividades')          
    return render(request=request,
                    template_name='atividades/proporatividade.html',
                    context={'form': changed_form,'schedules':schedules,'activity_sessions':changed_session,'espacos':espacos}
                    )
#-----------------EndDiogo------------------


#-----------------------David--------------------
def proporatividade(request):  
    if request.method == "POST":

        form_Sessao= SessaoForm(request.POST)
        form_Materiais= MateriaisForm(request.POST)
        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),
                             professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),
                             estado = "Pendente", diaabertoid = Diaaberto.objects.all().order_by('-id').first())
        formAtividade = AtividadeForm(request.POST, instance=new_form)

        if formAtividade.is_valid() and form_Sessao.is_valid() and form_Materiais.is_valid():
            new_form.save()  
            sessao = form_Sessao.save(commit= False)
            materiais = form_Materiais.save(commit= False)
            materiais.atividadeid = Atividade.objects.all().order_by('-id').first()
            materiais.save()
            sessao.vagas= sessao.participantesmaximo
            sessao.ninscritos= 0
            espacoid=request.POST.__getitem__('idespaco')
            sessao.espacoid= Espaco.objects.get(id=espacoid)
            horarioid=request.POST.__getitem__('idhorario')
            sessao.horarioid = Horario.objects.get(id=horarioid)
            sessao.save()
            new_as= Atividadesessao(atividadeid= Atividade.objects.all().order_by('-id').first(), sessaoid= Sessao.objects.all().order_by('-id').first())
            new_as.save()
            return HttpResponseRedirect('/thanks/')
        else:
            return render(request, 'atividades/inseriratividade.html',{'atividade': formAtividade , 'sessao': form_Sessao,'horario':  Horario.objects.all(), 'espaco': Espaco.objects.all(),'materiais': form_Materiais})
    else:  
        formAtividade = AtividadeForm()
        form_Sessao= SessaoForm()
        form_Materiais= MateriaisForm() 
    return render(request,'atividades/inseriratividade.html',{'atividade': formAtividade,'sessao': form_Sessao,'horario':  Horario.objects.all(), 'espaco': Espaco.objects.all, 'materiais': form_Materiais})  



def novasessao(request,id):  
    if request.method == "POST":

        form_Sessao= SessaoForm(request.POST)
        if  form_Sessao.is_valid(): 
            sessao = form_Sessao.save(commit= False)
            sessao.vagas= sessao.participantesmaximo
            sessao.ninscritos= 0
            sessao.espacoid= Espaco.objects.get(id=request.POST.__getitem__('idespaco'))
            sessao.horarioid = Horario.objects.get(id=request.POST.__getitem__('idhorario'))
            sessao.save()
            new_as= Atividadesessao(atividadeid= id, sessaoid= Sessao.objects.all().order_by('-id').first())
            new_as.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'atividades/sessao.html',{'sessao': form_Sessao,'horario':  Horario.objects.all(), 'espaco': Espaco.objects.all()})
    else:  
        form_Sessao= SessaoForm()
    return render(request,'atividades/sessao.html',{'sessao': form_Sessao,'horario':  Horario.objects.all(), 'espaco': Espaco.objects.all})  









#---------------------End David
    