from django.shortcuts import render, redirect  
from .forms import AtividadeForm , MateriaisForm, atividadesFilterForm, CampusForm
from .models import *
from configuracao.models import Horario
from .models import Atividade, Sessao, Tema
from coordenadores.models import Coordenador
from utilizadores.models import Professoruniversitario
from configuracao.models import Diaaberto, Horario, Campus, Edificio, Espaco
from django.http import HttpResponseRedirect
from datetime import datetime, date,timezone
from _datetime import timedelta
from django.db.models import Q
from django.core import serializers



#-------------Diogo----------------------
def login(request):
    return 0

def filters(request):
    filters=[]
    if request.POST.get('Aceite'):
        filters.append('Aceite')
    else:
        filters.append('')

    if request.POST.get('Recusada'):
        filters.append('Recusada')
    else:
        filters.append('')

    if request.POST.get('Pendente'):
        filters.append('Pendente')
    else:
        filters.append('')
    return filters

def minhasatividades(request):
    atividades=Atividade.objects.all()
    sessoes=Sessao.objects.all()
    if request.method == 'POST' or request.GET.get('searchAtividade'):
        today=datetime.now(timezone.utc)
        diaAberto=Diaaberto.objects.filter(datadiaabertofim__gte=today).first()
        filterForm=atividadesFilterForm(request.POST)
        nome=str(request.POST.get('searchAtividade'))
        atividades=atividades.filter(nome__icontains=nome)
        if request.POST.get('Aceite') or request.POST.get('Pendente') or request.POST.get('Recusada'):
            filter=filters(request)
            atividades=atividades.filter(Q(estado=filter[0]) | Q(estado=filter[1]) | Q(estado=filter[2]))
        if request.POST.get('diaAbertoAtual'):
            atividades=atividades.filter(diaabertoid=diaAberto)     
    else:
        filterForm=atividadesFilterForm()

    return render(request=request,
			template_name="atividades/minhasAtividades.html",
            context={"atividades": atividades,"sessoes":sessoes,"filter":filterForm})

def atividadescoordenador(request):
    atividades=Atividade.objects.all()
    sessoes=Sessao.objects.all()
    if request.method == 'POST' or request.GET.get('searchAtividade'):
        today=datetime.now(timezone.utc)
        diaAberto=Diaaberto.objects.filter(datadiaabertofim__gte=today).first()
        filterForm=atividadesFilterForm(request.POST)
        nome=str(request.POST.get('searchAtividade'))
        atividades=atividades.filter(nome__icontains=nome)
        tipo=str(request.POST.get('tipo'))
        departamento=str(request.POST.get('departamentos'))
        if tipo != ' ' and tipo != 'None':
            atividades=atividades.filter(tipo=tipo)
        if departamento != 'None' and departamento > '-1':
            print('departamento')
            atividades=atividades.filter(professoruniversitarioutilizadorid__departamento__id=departamento)
        if request.POST.get('Aceite') or request.POST.get('Pendente') or request.POST.get('Recusada'):
            print('estado')
            filter=filters(request)
            atividades=atividades.filter(Q(estado=filter[0]) | Q(estado=filter[1]) | Q(estado=filter[2]))
        if request.POST.get('diaAbertoAtual'):
            atividades=atividades.filter(diaabertoid=diaAberto)    
    else:
        filterForm=atividadesFilterForm()

    return render(request=request,
			template_name="atividades/atividadesUOrganica.html",
            context={"atividades": atividades,"sessoes":sessoes,"filter":filterForm})

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
#def proporatividade(request): 
#    #espacodisponivel= []
#    
#    #for esp in Espaco.objects.all():
#    #    Atividadeespaco= Atividade.objects.all().filter(espacoid=esp.id)
#    #    total=0
#    #    for espAtv in Atividadeespaco:
#    #       Sessoes= len(Sessao.objects.all().filter(atividadeid= espAtv))
#    #       total+=Sessoes
#    #    if total!= len(Horario.objects.all()):
#    #        espacodisponivel.append(Espaco.objects.get(id=esp.id))
#    #espacos = Espaco.objects.all()  
#    today= datetime.now(timezone.utc) 
#    diaaberto=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)
#    #print("datahoje"+datahoje)      
#    if request.method == "POST":
#        if 'veredificios' in request.POST:
#            veredificios(request)
#        print(request.POST['edificioid'])
#        #print(request.POST['espaco'])
#        form_Materiais= MateriaisForm(request.POST)
#        #new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),
#        #                     professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),
#        #                     estado = "Pendente", diaabertoid = diaaberto,espacoid= Espaco.objects.get(id=request.POST['espacoid']),
#        #                     tema=Tema.objects.get(id=request.POST['tema']))
#        #formAtividade = AtividadeForm(request.POST, instance=new_form)
#        
#        if formAtividade.is_valid() and  form_Materiais.is_valid():
#            
#            new_form.save()  
#            materiais = form_Materiais.save(commit= False)
#            materiais.atividadeid = Atividade.objects.all().order_by('-id').first()
#            materiais.save()
#            idAtividade= Atividade.objects.all().order_by('-id').first()
#            return redirect('inserirSessao', idAtividade.id)
#    else:  
#        formAtividade = AtividadeForm()
#        form_Materiais= MateriaisForm() 
#    edi=Edificio.objects.all()
#    camps=Campus.objects.all()
#    esp=Espaco.objects.all()
#    edificios_json=serializers.serialize("json",list(edi) )
#    campus_json=serializers.serialize("json",list(camps))
#    espaco_json=serializers.serialize("json", list(esp)) 
#    return render(request,'atividades/proporAtividadeAtividade.html',{'form': formAtividade,'campu':-1, "campus_json":campus_json, 'campus': Campus.objects.all(), "edificios_json":edificios_json, 'edificios': Edificio.objects.all(),"espaco_json":espaco_json,'espacos': Espaco.objects.all(),'mat': form_Materiais})  


def proporatividade(request):
    today= datetime.now(timezone.utc) 
    diaaberto=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)
    if request.method == "POST":

        print(diaaberto.id)


        activity_object_form = AtividadeForm(request.POST)
        campusid= request.POST["campusid"]
        campu= Campus.objects.get(id=campusid)
        campus=Campus.objects.all().exclude(id=campusid)
        Edificios= Edificio.objects.filter(campus=campusid)

        if 'veredificios' in request.POST:    
            activity_object_form=AtividadeForm(request.POST)
            print(activity_object_form)
            return render(request,'atividades/proporAtividadeAtividade.html',{'form': activity_object_form,'campu':campu, 'campus': campus, 'edificios': Edificios,'espacos': ""})

        
        if 'versala' in request.POST:
            edificioid=request.POST["edificioid"]
            sala= Edificio.objects.get(id=edificioid)
            salas= Espaco.objects.filter(edificio=sala).exclude(id=edificioid)
            return render(request,'atividades/proporAtividadeAtividade.html',{'form': activity_object_form, 'campu':campu, 'campus': campus,'edificio':sala,'edificios': Edificios,'espacos': salas})

        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),
                             professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),
                             estado = "Pendente", diaabertoid = diaaberto,espacoid= Espaco.objects.get(id=request.POST['espacoid']),
                             tema=Tema.objects.get(id=request.POST['tema']))
        activity_object_form = AtividadeForm(request.POST, instance=new_form)
        if activity_object_form.is_valid():
            activity_object_form.save()
            idAtividade= Atividade.objects.all().order_by('-id').first()
            return redirect('inserirSessao', idAtividade.id)
    else:  
        activity_object_form= AtividadeForm()
    return render(request,'atividades/proporAtividadeAtividade.html',{'form': activity_object_form,'campu':-1,'campus': Campus.objects.all(), 'edificios': "",'espacos': ""})


    
      
#def inserirsessao(request,id):
#    disp= []
#    horariosindisponiveis= []
#    #espaco_id= Atividade.objects.get(id=id).espacoid # Busca o espaco da atividade
#    #espacoidtest= espaco_id.id #  Busca o id do espaco
#    ##print(espacoidtest)
#    #atividadescomespaco_id=Atividade.objects.all().filter(espacoid=espacoidtest).exclude(id=id) # Busca as atividades com o espaco da atividade
#    ##print(atividadescomespaco_id)
##
##
#    #idAtividades= []
#    #for atv_id in atividadescomespaco_id: 
#    #    idAtividades.append(atv_id.id) # Busca o id das atividades
#    ##print(idAtividades)
##
#    #sessao_espaco= []
#    #for sessao in idAtividades:
#    #    print(sessao)
#    #    sessao_espaco.append(Sessao.objects.all().filter(atividadeid=sessao)) # Busca as sessoes das atividades
#    ##print(sessao_espaco)
#    #for sessao in sessao_espaco:
#    #    for sessao2 in sessao:
#    #        horariosindisponiveis.append(sessao2.horarioid)
#    ##print(horariosindisponiveis)
#    today= datetime.now(timezone.utc) 
#    diaaberto=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)
#    diainicio= diaaberto.datadiaabertoinicio.date()
#    diafim= diaaberto.datadiaabertofim.date()
#    totaldias= diafim-diainicio
#    #print(totaldias.days)
#    dias_diaaberto= []
#    for d in range(totaldias.days):
#        dias_diaaberto.append(diainicio+timedelta(days=d))
#    #print(dias_diaaberto)
#    #sessao_indis= Sessao.objects.all().filter(atividadeid=id)
#
#    #for sessao in sessao_indis:
#    #    horariosindisponiveis.append(sessao.horarioid)
#    ##print(horariosindisponiveis)
#    #horariosindisponiveis= list(dict.fromkeys(horariosindisponiveis))
##
#    #for t in Horario.objects.all():
#    #    if  t not in horariosindisponiveis:
#    #        disp.append(t)
##
#        
#    if request.method == "POST":
#
#        if 'ver' in request.POST:
#            diasessao=request.POST['diasessao'] 
#            sessoes= Sessao.objects.all().filter(atividadeid=id, dia=diasessao)
#            for sessao in sessoes:
#                horariosindisponiveis.append(sessao.horarioid)
#            #print(horariosindisponiveis)
#            horariosindisponiveis= list(dict.fromkeys(horariosindisponiveis))
#
#            for t in Horario.objects.all():
#                if  t not in horariosindisponiveis:
#                    disp.append(t)
#        return render(request,'atividades/proporAtividadeSessao.html',{'horarios': disp , 'sessions_activity': Sessao.objects.all().filter(atividadeid= id), 'dias':dias_diaaberto}) 
#
#        if 'save' in request.POST and len(sessoes)!=0 :
#            return redirect('minhasAtividades')
#        elif 'save' in request.POST and len(sessoes)==0:
#            return redirect('inserirSessao', id)
#        new_Sessao= Sessao(vagas=Atividade.objects.get(id= id).participantesmaximo,ninscritos=0 ,horarioid=Horario.objects.get(id=request.POST['horarioid']), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
#        new_Sessao.save()
#        if 'cancelar' in request.POST :
#            Atividade.objects.get(id=id).delete()
#            return redirect('proporAtividade')
#        elif 'new' in request.POST:
#            return redirect('inserirSessao', id)
#    return render(request,'atividades/proporAtividadeSessao.html',{'horarios': "Escolha primeiro um dia" , 'sessions_activity': Sessao.objects.all().filter(atividadeid= id), 'dias':dias_diaaberto}) 


def inserirsessao(request,id):
    today= datetime.now(timezone.utc) 
    diaaberto=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)
    diainicio= diaaberto.datadiaabertoinicio.date()
    diafim= diaaberto.datadiaabertofim.date()
    totaldias= diafim-diainicio
    dias_diaaberto= []
    for d in range(totaldias.days):
        dias_diaaberto.append(diainicio+timedelta(days=d))



    horariosindisponiveis= []
    disp= []
    if request.method == "POST":
        atividadeid=Atividade.objects.get(id=id)
        if 'ver' in request.POST:
            diasessao=request.POST["diasessao"]
            print(diasessao)
            sessaodia=Sessao.objects.filter(atividadeid=id, dia=diasessao)
            for sessao in sessaodia:
                horariosindisponiveis.append(sessao.horarioid)
            for t in Horario.objects.all():
                if  t not in horariosindisponiveis:
                    disp.append(t)
            print(disp)
            return render(request,'atividades/proporAtividadeSessao.html',{'horarios': disp , 'sessao': diasessao, 'sessions_activity': Sessao.objects.all().filter(atividadeid= id), 'dias': dias_diaaberto }) 
        sessoes=Sessao.objects.all().filter(atividadeid=id)
        if 'save' in request.POST and len(sessoes)!=0 :
            return redirect('minhasAtividades')
        if 'save' in request.POST and len(sessoes)==0:
            return redirect('inserirSessao', id)
        if 'cancelar' in request.POST :
            Atividade.objects.get(id=id).delete()
            return redirect('proporAtividade')
        if 'new' in request.POST:
            diasessao=request.POST["diasessao"]
            print(diasessao)
            new_Sessao= Sessao(vagas=Atividade.objects.get(id= id).participantesmaximo,ninscritos=0 ,horarioid=Horario.objects.get(id=request.POST['horarioid']), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
            new_Sessao.save()
            return redirect('inserirSessao', id)
    return render(request,'atividades/proporAtividadeSessao.html',{'horarios': "" , 'sessions_activity': Sessao.objects.all().filter(atividadeid= id), 'dias': dias_diaaberto})        




def validaratividade(request,id, action):
    atividade=Atividade.objects.get(id=id)
    if action==0:
        atividade.estado='Recusada'
    if action==1:
        atividade.estado='Aceite'
    atividade.save()
    return redirect('minhasAtividades')

#---------------------End David
    
def load_campus(request):
    campus_id = request.GET.get('campusid')
    cities = Campus.objects.filter(id=campus_id.id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})
