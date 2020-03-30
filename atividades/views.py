from django.shortcuts import render, redirect  
from .forms import AtividadeForm , MateriaisForm
from .models import *
from configuracao.models import Horario
from .models import Atividade, Espaco, Sessao, Tema
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
















#-----------------EndDiogo------------------


#-----------------------David--------------------
def inseriratividade(request):  
    if request.method == "POST":
        form_Materiais= MateriaisForm(request.POST)
        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),
                             professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),
                             estado = "Pendente", diaabertoid = Diaaberto.objects.all().order_by('-id').first(),espacoid= Espaco.objects.get(id=request.POST['idespaco']),
                             tema=Tema.objects.get(id=request.POST['idtema']))
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
    horariosindisponiveis= []
    espaco_id= Atividade.objects.get(id=id).espacoid # Busca o espaco da atividade
    espacoidtest= espaco_id.id #  Busca o id do espaco
    #print(espacoidtest)
    atividadescomespaco_id=Atividade.objects.all().filter(espacoid=espacoidtest).exclude(id=id) # Busca as atividades com o espaco da atividade
    #print(atividadescomespaco_id)


    idAtividades= []
    for atv_id in atividadescomespaco_id: 
        idAtividades.append(atv_id.id) # Busca o id das atividades
    print(idAtividades)

    sessao_espaco= []
    for sessao in idAtividades:
        print(sessao)
        sessao_espaco.append(Sessao.objects.all().filter(atividadeid=sessao)) # Busca as sessoes das atividades
    print(sessao_espaco)
    for sessao in sessao_espaco:
        for sessao2 in sessao:
            horariosindisponiveis.append(sessao2.horarioid)
    print(horariosindisponiveis)

    sessao_indis= Sessao.objects.all().filter(atividadeid=id)
    for sessao in sessao_indis:
        horariosindisponiveis.append(sessao.horarioid)
    #print(horariosindisponiveis)
    horariosindisponiveis= list(dict.fromkeys(horariosindisponiveis))

    for t in Horario.objects.all():
        if  t not in horariosindisponiveis:
            disp.append(t)
    if len(disp)==0:
        Atividade.objects.get(id=id).delete()
        return redirect('inserirAtividade') 
        
    if request.method == "POST":
            new_Sessao= Sessao(vagas=Atividade.objects.get(id= id).participantesmaximo,ninscritos=0 ,horarioid=Horario.objects.get(id=request.POST['idhorario']), atividadeid=Atividade.objects.get(id=id))
            new_Sessao.save()
            if 'save' in request.POST :
                return HttpResponseRedirect('/thanks/')
            elif 'new' in request.POST:
                return redirect('inserirSessao', id)
    return render(request,'atividades/inserirsessao.html',{'horario': disp })  






#---------------------End David
    