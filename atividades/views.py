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
    activity_session_object = Atividadesessao.objects.all().filter(atividadeid=id).first() #Dupla (sessao,atividade)
    session_object = activity_session_object.sessaoid #Sessao na dupla
    activity_object = activity_session_object.atividadeid #Objecto da atividade que temos de mudar, ativdade da dupla
    activity_object_form = AtividadeForm(instance=activity_object) #Formulario instanciado pela atividade a mudar
    #-----------------------------
    session_object_form = SessaoForm(instance=session_object)

    if request.method == 'POST':    #Se estivermos a receber um request com formulario

        activity_object_form = AtividadeForm(request.POST, instance=activity_object)
        session_object.horarioid = Horario.objects.get(id=int(request.POST['horarioid']))
        session_object.espacoid = Espaco.objects.get(id=int(request.POST['espacoid']))
        session_object.participantesmaximo = int(request.POST['participantesmaximo'])

        if activity_object_form.is_valid():
                #-------Guardar as mudancas a atividade em si------
                activity_object_formed = activity_object_form.save(commit=False)
                
                activity_object_formed.estado = "Pendente"
                activity_object_formed.dataalteracao = datetime.now()
                activity_object_formed.save()
                #--------Guardas as mudancas da sessao em si-------
                session_object.save()
                #---------------------------------------------------

                return HttpResponseRedirect('/minhasatividades')          
    return render(request=request,
                    template_name='atividades/proporatividade.html',
                    context={'form': activity_object_form,'sessao_form':session_object_form}
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
    