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
def minhasatividades(request):
    	return render(request=request,
				template_name="atividades/listaAtividades.html",
                context={"atividades": Atividade.objects.all()})

def alterarAtividade(request,id):
    #------atividade a alterar----
    activity_object = Atividade.objects.get(id=id) #Objecto da atividade que temos de mudar, ativdade da dupla
    activity_object_form = AtividadeForm(instance=activity_object) #Formulario instanciado pela atividade a mudar
    espaco= Espaco.objects.get(id=activity_object.espacoid.id)
    #print(espaco)
    espacos = Espaco.objects.all()
    #print(espacos)
    #-----------------------------
    if request.method == 'POST':    #Se estivermos a receber um request com formulario  
        submitted_data = request.POST.copy()
        activity_object.tema = Tema.objects.get(id=int(request.POST['tema']))
        activity_object_form = AtividadeForm(submitted_data, instance=activity_object)
        if activity_object_form.is_valid():
                #-------Guardar as mudancas a atividade em si------
                activity_object_formed = activity_object_form.save(commit=False)  
                activity_object_formed.estado = "Pendente"
                activity_object_formed.dataalteracao = datetime.now()
                activity_object_formed.save()
                return redirect('inserirSessao',id)          
    return render(request=request,
                    template_name='atividades/proporAtividadeAtividade.html',
                    context={'form': activity_object_form, 'espaco':espaco,'espacos':espacos}
                    )

def eliminarAtividade(request,id):
    Atividade.objects.get(id=id).delete() #Dupla (sessao,atividade)
    return HttpResponseRedirect('/minhasatividades')

#def alterarSessao(request,id):
#    sessions_activity = Sessao.objects.filter(atividadeid=id)
#    horarios = Horario.objects.all()
#    if request.method == 'POST':
#        submitted_data = request.POST.copy()
#        submitted_data['horarioid']=Horario.objects.get(id=request.POST['horarioid'])
#        new_Sessao= Sessao(vagas=Atividade.objects.get(id= id).participantesmaximo,
#            ninscritos=0 ,horarioid=submitted_data['horarioid'], atividadeid=Atividade.objects.get(id=id))
#        new_Sessao.save()
#        return redirect('alterarSessao',id)
#    return render(request=request,
#                    template_name='atividades/proporAtividadeSessao.html',
#                    context={'sessions_activity': sessions_activity,'horarios':horarios,'atividadeid':id}
#                    )

def eliminarSessao(request,id):
    atividadeid=Sessao.objects.get(id=id).atividadeid.id
    Sessao.objects.get(id=id).delete()
    return redirect('inserirSessao',atividadeid)
#-----------------EndDiogo------------------


#-----------------------David--------------------
def proporatividade(request): 
    #espacodisponivel= []
    
    #for esp in Espaco.objects.all():
    #    Atividadeespaco= Atividade.objects.all().filter(espacoid=esp.id)
    #    total=0
    #    for espAtv in Atividadeespaco:
    #       Sessoes= len(Sessao.objects.all().filter(atividadeid= espAtv))
    #       total+=Sessoes
    #    if total!= len(Horario.objects.all()):
    #        espacodisponivel.append(Espaco.objects.get(id=esp.id))
    espacos = Espaco.objects.all()  
             
    if request.method == "POST":
        form_Materiais= MateriaisForm(request.POST)
        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),
                             professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),
                             estado = "Pendente", diaabertoid = Diaaberto.objects.get(id=3),espacoid= Espaco.objects.get(id=request.POST['espacoid']),
                             tema=Tema.objects.get(id=request.POST['tema']))
        formAtividade = AtividadeForm(request.POST, instance=new_form)
        
        if formAtividade.is_valid() and  form_Materiais.is_valid():
            
            new_form.save()  
            materiais = form_Materiais.save(commit= False)
            materiais.atividadeid = Atividade.objects.all().order_by('-id').first()
            materiais.save()
            idAtividade= Atividade.objects.all().order_by('-id').first()
            return redirect('inserirSessao', idAtividade.id)
        else:
            return render(request, 'atividades/proporAtividadeAtividade.html',{'form': formAtividade,'espaco': -1, 'espacos': espacos, 'mat': form_Materiais})
    else:  
        formAtividade = AtividadeForm()
        form_Materiais= MateriaisForm() 
    return render(request,'atividades/proporAtividadeAtividade.html',{'form': formAtividade,'espaco': -1, 'espacos': espacos, 'mat': form_Materiais})  



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
    #print(idAtividades)

    sessao_espaco= []
    for sessao in idAtividades:
        print(sessao)
        sessao_espaco.append(Sessao.objects.all().filter(atividadeid=sessao)) # Busca as sessoes das atividades
    #print(sessao_espaco)
    for sessao in sessao_espaco:
        for sessao2 in sessao:
            horariosindisponiveis.append(sessao2.horarioid)
    #print(horariosindisponiveis)

    sessao_indis= Sessao.objects.all().filter(atividadeid=id)
    for sessao in sessao_indis:
        horariosindisponiveis.append(sessao.horarioid)
    #print(horariosindisponiveis)
    horariosindisponiveis= list(dict.fromkeys(horariosindisponiveis))

    for t in Horario.objects.all():
        if  t not in horariosindisponiveis:
            disp.append(t)

        
    if request.method == "POST":
        sessoes= Sessao.objects.all().filter(atividadeid=id)
        if 'save' in request.POST and len(sessoes)!=0 :
            return redirect('minhasAtividades')
        elif 'save' in request.POST and len(sessoes)==0:
            return redirect('inserirSessao', id)
        new_Sessao= Sessao(vagas=Atividade.objects.get(id= id).participantesmaximo,ninscritos=0 ,horarioid=Horario.objects.get(id=request.POST['horarioid']), atividadeid=Atividade.objects.get(id=id))
        new_Sessao.save()
        if 'cancelar' in request.POST :
            return redirect('proporAtividade')
        elif 'new' in request.POST:
            return redirect('inserirSessao', id)
    return render(request,'atividades/proporAtividadeSessao.html',{'horarios': disp , 'sessions_activity': Sessao.objects.all().filter(atividadeid= id)}) 

#---------------------End David
    