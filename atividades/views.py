from django.shortcuts import render, redirect  
from .forms import AtividadeForm , MateriaisForm, atividadesFilterForm, CampusForm
from .models import *
from configuracao.models import Horario
from .models import Atividade, Sessao, Tema, Materiais
from utilizadores.models import ProfessorUniversitario, Coordenador
from configuracao.models import Campus, Departamento, Diaaberto, Edificio, Espaco, Horario
from django.http import HttpResponseRedirect
from datetime import datetime, date,timezone
from _datetime import timedelta
from django.db.models import Q
from django.core import serializers
from django.forms.models import modelformset_factory
from django.forms.widgets import Select
from atividades.forms import SessaoForm

from notificacoes import views as nviews
from utilizadores import views as uviews



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
    
    user_check_var = uviews.user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    atividades=Atividade.objects.filter(professoruniversitarioutilizadorid=ProfessorUniversitario.objects.get(utilizador_ptr_id = request.user.id)).exclude(estado="nsub")
    sessoes=Sessao.objects.all()
    materiais= Materiais.objects.all()
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
            context={"atividades": atividades,"sessoes":sessoes,"materiais": materiais,"filter":filterForm})

class Conflito:
    def __init__(self, atividade1,atividade2):
        self.atividade1=atividade1
        self.atividade2=atividade2
        

def atividadescoordenador(request):
    user_check_var = uviews.user_check(request=request, user_profile=[Coordenador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    today= datetime.now(timezone.utc) - timedelta(hours=1, minutes=00)
    print(today)
    Atividade.objects.filter(estado="nsub",datasubmissao__lte=today).delete()
        
    atividades=Atividade.objects.filter(professoruniversitarioutilizadorid__faculdade_id=Coordenador.objects.get(utilizador_ptr_id = request.user.id).faculdade).exclude(estado="nsub")
    departamentos= Departamento.objects.filter(unidadeorganicaid= Coordenador.objects.get(utilizador_ptr_id = request.user.id).faculdade)
    dep= -1

    sessoes=Sessao.objects.all()
    materiais= Materiais.objects.all()
    conflito2= []
    for sessao1 in sessoes:
        for sessao2 in sessoes:
            if sessao1.id!=sessao2.id and sessao1.atividadeid!= sessao2.atividadeid and sessao1.atividadeid.espacoid == sessao2.atividadeid.espacoid and sessao1.dia == sessao2.dia:     
                    hora1inicio=sessao1.horarioid.inicio.hour*60+sessao1.horarioid.inicio.minute
                    hora1fim=sessao1.horarioid.fim.hour*60+sessao1.horarioid.fim.minute
                    hora2inicio=sessao2.horarioid.inicio.hour*60+sessao2.horarioid.inicio.minute
                    hora2fim=sessao2.horarioid.fim.hour*60+sessao2.horarioid.fim.minute
                    if hora1inicio<=hora2inicio < hora1fim or hora1inicio< hora2fim <= hora1fim:
                        C1=Conflito(sessao1.atividadeid,sessao2.atividadeid)
                        conflito2.append(C1)
    conflito2= list(dict.fromkeys(conflito2))
    #for c in conflito2:
    #    print(c.atividade1)                
    if request.method == 'POST' or request.GET.get('searchAtividade'):
        today=datetime.now(timezone.utc)
        diaAberto=Diaaberto.objects.filter(datadiaabertofim__gte=today).first()
        filterForm=atividadesFilterForm(request.POST)
        nome=str(request.POST.get('searchAtividade'))
        atividades=atividades.filter(nome__icontains=nome)
        tipo=str(request.POST.get('tipo'))
        departamento=str(request.POST.get('departamentos'))
        if request.POST.get('departamentos') is not "":
            dep=Departamento.objects.filter(id=request.POST.get('departamentos')).first()
        if dep is None:
            dep= -1
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
            context={"atividades": atividades,"conflitos":conflito2,"sessoes":sessoes,"materiais": materiais,"filter":filterForm, "dep":dep,"departamentos":departamentos})


def alterarAtividade(request,id):
    user_check_var = uviews.user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    if atividade.exists():  
        activity_object = Atividade.objects.get(id=id) #Objecto da atividade que temos de mudar, ativdade da dupla
        if activity_object.professoruniversitarioutilizadorid != ProfessorUniversitario.objects.get(utilizador_ptr_id = request.user.id):
            return redirect("utilizadores:home")
        #------atividade a alterar----
        activity_object = Atividade.objects.get(id=id) #Objecto da atividade que temos de mudar, ativdade da dupla
        activity_object_form = AtividadeForm(instance=activity_object) #Formulario instanciado pela atividade a mudar
        espaco= Espaco.objects.get(id=activity_object.espacoid.id)
        materiais_object= Materiais.objects.get(atividadeid=id)
        new_material = Materiais(atividadeid=activity_object, nomematerial= materiais_object)
        materiais_object_form= MateriaisForm(instance=materiais_object)
        campusid= espaco.edificio.campus.id
        campus= Campus.objects.all().exclude(id=campusid)

        edificioid= espaco.edificio.id
        edificios= Edificio.objects.filter(campus=campusid).exclude(id=edificioid)

        espacos= Espaco.objects.filter(edificio=edificioid).exclude(id=espaco.id)
        #print(espaco)
        #print(espacos)
        #-----------------------------
        if request.method == 'POST':    #Se estivermos a receber um request com formulario  
            submitted_data = request.POST.copy()
            activity_object.tema = Tema.objects.get(id=int(request.POST['tema']))
            activity_object_form = AtividadeForm(submitted_data, instance=activity_object)
            materiais_object_form = MateriaisForm(request.POST, instance=materiais_object)
            if activity_object_form.is_valid() and materiais_object_form.is_valid():
                    #-------Guardar as mudancas a atividade em si------
                    activity_object_formed = activity_object_form.save(commit=False) 
                    if  activity_object_formed.estado == "nsub":
                        activity_object_formed.estado = "nsub"
                        activity_object_formed.save()
                        materiais_object_form.save()
                    else:
                        print("hello")
                        print(Atividade.objects.get(id=id) == activity_object_formed)
                        if Atividade.objects.get(id=id) != activity_object_formed or Materiais.objects.get(atividadeid=id) != materiais_object_form.instance:
                            activity_object_formed.estado = "Pendente"
                            activity_object_formed.dataalteracao = datetime.now()
                            activity_object_formed.save()
                            materiais_object_form.save()
                    #views.enviar_notificacao_automatica(request,"atividadeAlterada",id) #Enviar Notificacao Automatica !!!!!!
                    return redirect('atividades:inserirSessao',id)          
        return render(request=request,
                        template_name='atividades/proporAtividadeAtividade.html',
                        context={'form': activity_object_form, 'espaco':espaco,'espacos':espacos, "edificios": edificios, "campus":campus, "materiais":materiais_object_form}
                        )
    else:
        return redirect('atividades:minhasAtividades')

def eliminarAtividade(request,id):
    user_check_var = uviews.user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    if atividade.exists():
        atividade.delete()
        #nviews.enviar_notificacao_automatica(request,"atividadeApagada",id) #Enviar Notificacao Automatica !!!!!!
    return redirect('atividades:minhasAtividades')
    



def eliminarSessao(request,id):
    user_check_var = uviews.user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')
    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    sessoes = Sessao.objects.filter(id=id,atividadeid__professoruniversitarioutilizadorid=userId)

    if sessoes.exists():
        sessaor=sessoes.first()
        atividadeid= sessaor.atividadeid.id
        sessaor.delete()
        return redirect('atividades:inserirSessao',atividadeid)
    return redirect('atividades:minhasAtividades')


def proporatividade(request):
    
    user_check_var = uviews.user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    today= datetime.now(timezone.utc) 
    diaabertopropostas=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)

    
    diainicio= diaabertopropostas.datadiaabertoinicio.date()
    diafim= diaabertopropostas.datadiaabertofim.date()
    totaldias= diafim-diainicio+timedelta(days=1)
    dias_diaaberto= []
    for d in range(totaldias.days):
        dias_diaaberto.append(diainicio+timedelta(days=d))

    sessoes= ""
    if request.method == "POST":
        
        activity_object_form = AtividadeForm(request.POST)
        campus=Campus.objects.all()
        activity_object_form = AtividadeForm(request.POST)
        material_object_form= MateriaisForm(request.POST)
        if activity_object_form.is_valid():  
            espacoid=request.POST["espacoid"] 
            espaco=Espaco.objects.get(id=espacoid)  
        else:
            return render(request,'atividades/testAtividades.html',{'form': activity_object_form,'campus': Campus.objects.all(),"materiais": material_object_form,
                            'horarios': "" , 'sessions_activity':sessoes, 'dias': dias_diaaberto, "id":-1,"style1": "", "style2":"display:none"
                            })   
        if "new" in request.POST:
            print("new")
            new_form = Atividade(professoruniversitarioutilizadorid = ProfessorUniversitario.objects.get(utilizador_ptr_id = request.user.id),
                             estado = "nsub", diaabertoid = diaabertopropostas,espacoid= Espaco.objects.get(id=espaco.id),
                             tema=Tema.objects.get(id=request.POST['tema']))
            activity_object_form = AtividadeForm(request.POST, instance=new_form)
            activity_object_form.save()
            idAtividade= Atividade.objects.all().order_by('-id').first()
            new_material= Materiais(atividadeid=idAtividade)
            material_object_form= MateriaisForm(request.POST, instance= new_material)
            material_object_form.save()
            diasessao=request.POST["diasessao"]
            inicio= request.POST['horarioid']
            splitinicio=inicio.split(":")
            print(splitinicio)
            duracaoesperada= idAtividade.duracaoesperada
            hfim= horariofim(splitinicio,duracaoesperada)
            horario= Horario.objects.filter(inicio= request.POST['horarioid'], fim=hfim).first()
            if horario is None:
                new_Horario= Horario(inicio=inicio, fim=hfim)
                new_Horario.save()
            else:
                new_Horario= horario
            new_Sessao= Sessao(vagas=idAtividade.participantesmaximo,ninscritos=0 ,horarioid=Horario.objects.get(id=new_Horario.id), atividadeid=idAtividade,dia=diasessao)
            new_Sessao.save()
            return redirect('atividades:inserirSessao', idAtividade.id)
    else:
        material_object_form= MateriaisForm() 
        activity_object_form= AtividadeForm()
    return render(request,'atividades/testAtividades.html',{'form': activity_object_form,'campus': Campus.objects.all(),"materiais": material_object_form,
                            'horarios': "" , 'sessions_activity':sessoes, 'dias': dias_diaaberto, "id":-1, "style1": "", "style2":"display:none"
                            })




def horariofim(inicio,duracao):
    calculo= int(inicio[0])*60+ int(inicio[1])+duracao
    hora=int(calculo/60)
    minutos= int(calculo%60)
    fim= str(hora)+":"+str(minutos)
    return fim

def inserirsessao(request,id):

    user_check_var = uviews.user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    if atividade.exists():  
        today= datetime.now(timezone.utc) 
        diaaberto=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)
        diainicio= diaaberto.datadiaabertoinicio.date()
        diafim= diaaberto.datadiaabertofim.date()
        totaldias= diafim-diainicio+timedelta(days=1)
        dias_diaaberto= []
        for d in range(totaldias.days):
            dias_diaaberto.append(diainicio+timedelta(days=d))
        horariosindisponiveis= []
        disp= []
        atividadeid=Atividade.objects.get(id=id)
        sessoes=Sessao.objects.all().filter(atividadeid=id)
        check= len(sessoes)
        if request.method == "POST":
            if 'proximo' in request.POST:
                return redirect('atividades:verResumo', id)
            if 'anterior' in request.POST :
                return redirect('atividades:alterarAtividade',id)
            if 'new' in request.POST:
                diasessao=request.POST["diasessao"]
                print(diasessao)
                inicio= request.POST['horarioid']
                splitinicio=inicio.split(":")
                print(splitinicio)
                duracaoesperada= atividadeid.duracaoesperada
                hfim= horariofim(splitinicio,duracaoesperada)
                horario= Horario.objects.filter(inicio= request.POST['horarioid'], fim=hfim).first()
                if horario is None:
                    new_Horario= Horario(inicio=inicio, fim=hfim)
                    new_Horario.save()
                else:
                    new_Horario= horario
                new_Sessao= Sessao(vagas=Atividade.objects.get(id= id).participantesmaximo,ninscritos=0 ,horarioid=Horario.objects.get(id=new_Horario.id), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
                if atividadeid.estado != "nsub":
                    atividadeid.estado= "Pendente"
                atividadeid.save()
                new_Sessao.save()
                return redirect('atividades:inserirSessao', id)
        return render(request=request,
                      template_name='atividades/proporAtividadeSessao.html',
                      context={'horarios': "" , 
                               'sessions_activity': Sessao.objects.all().filter(atividadeid= id), 
                               'dias': dias_diaaberto,
                               'check': check, "id":id})
    else:
        return redirect('atividades:minhasAtividades')    


class TimeC():
    time: str = None
    seconds: int = None
    time_split = None

    def __init__(self, time:str = None, time_as_seconds: int = None):
        if time is not None and time_as_seconds is not None:
            raise Exception('Only one argument can be set')
        if time is None and time_as_seconds is None:
            raise Exception('Either argument must be set')
        if time is not None:
            self.time = time
            self.time_split = str(time).split(':')
            self.seconds = int(self.time_split[0])*60*60 + int(self.time_split[1])*60
            self.__str__()
        else:
            self.time = str(int(time_as_seconds/60/60)) + ':' + str(int(time_as_seconds%3600))
            self.seconds = time_as_seconds
            self.time_split = self.time.split(':')
            self.__str__()


    def __add__(self, other):
        time_s = other.seconds
        time_sum = self.seconds+time_s
        if time_sum >= 86400:
            time_sum-=86400
        return TimeC(time_as_seconds=time_sum)

    def __sub__(self, other):
        time_s = other.seconds
        time_sub = self.seconds-time_s
        if time_sub < 0:
            time_sub=0
        return TimeC(time_as_seconds=time_sub)

    def __str__(self):
        if (len(self.time_split[0]) == 1): time_start = '0' + str(self.time_split[0]) 
        else: time_start = self.time_split[0]
        if (len(self.time_split[1]) == 1): time_end =  self.time_split[1] + '0'
        else: time_end =  self.time_split[1]
        self.time= time_start+':'+time_end
        return self.time


    def __eq__(self, other):
        return other.__str__() == self.__str__()
    def __lt__(self, other):
        return self.seconds < other.seconds
    def __gt__(self, other):
        return self.seconds > other.seconds
    def __le__(self, other):
        return self.seconds <= other.seconds
    def __ge__(self, other):
        return self.seconds >= other.seconds    
    def __ne__(self, other):
        return not self.__eq__(self,other=other)





def sessaoRow(request):
    value = int(request.POST.get('extra'))
    dias = Diaaberto.objects.get(datapropostasatividadesincio__lte=datetime.now(),dataporpostaatividadesfim__gte=datetime.now()).days_as_array()
    data = {
		'form_dia': "form-" + str(value-1) + "-dia",
		'form_dia': "form-" + str(value-1) + "-dia",
		'form_horario': "form-" + str(value-1) + "-horarioid",
		'form_horario': "form-" + str(value-1) + "-horarioid",
		'form_id': 'form-' + str(value-1) + '-id',
        'dias': dias,
	}
    return render(request=request, template_name='atividades/sessaoRow.html', context=data)

def veredificios(request):
    campus=request.POST["valuecampus"]
    edificios = Edificio.objects.filter(campus=campus)
    print(request.POST["valuecampus"])
    print(edificios)
    return render(request, template_name="atividades/generic_list_options.html", context={"generic": edificios})

def versalas(request):
    edificios=request.POST["valueedificio"]
    print(request.POST["valueedificio"])
    salas = Espaco.objects.filter(edificio=edificios)
    return render(request, template_name="atividades/generic_list_options.html", context={"generic": salas})


class Chorarios:
    def __init__(self, inicio,fim):
        self.inicio=inicio
        self.fim=fim


def verhorarios(request):
    horarios=[]
    #horarioindisponivel = request.POST['horarioindisponivel[]']
    #print(horarioindisponivel)
    today = datetime.now(timezone.utc)

    default = {
        'key': '',
        'value': 'Escolha um horario'
    }

    diasessao=request.POST["valuedia"]
    id= request.POST["id"]
    print(id)
    if id != -1:
        sessaodia=Sessao.objects.filter(atividadeid=id, dia=diasessao)

        print(sessaodia)
        horar= []
        horariosindisponiveis= []
        horar2= []
        horar3= []
        escala=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today).escalasessoes.minute
        print(escala)
        if len(sessaodia)==0:
            options = [{
            'key': str(session_time),
            'value': str(session_time),
            } for session_time in Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today).session_times()]
        else:
            for sessao in sessaodia:
                timeinicio= TimeC(time=str(sessao.horarioid.inicio.hour)+":"+str(sessao.horarioid.inicio.minute))
                timefim= TimeC(time=str(sessao.horarioid.fim.hour)+":"+str(sessao.horarioid.fim.minute))    
                hor= Chorarios(timeinicio,timefim)
                horariosindisponiveis.append(hor)
            #print(horariosindisponiveis)
            
            for session_time in Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today).session_times():
                timelist= TimeC(time=str(session_time))
                horar.append(timelist)

        
            #print(horar)
            for h in horar:             
                for s in horariosindisponiveis:
                    print("inicio:"+ str(s.inicio) )
                    if h >= s.inicio and h < s.fim:
                        horar2.append(h)

            for h in horar:
                if h not in horar2:
                    horar3.append(h)
            options = [{
                'key': str(session_time),
                'value': str(session_time),
            } for session_time in horar3]

    else:       
        options = [{
            'key': str(session_time),
            'value': str(session_time),
        } for session_time in Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today).session_times()]

    return render(request=request, 
                template_name="configuracao/dropdown.html", 
                context={"options": options,    "default": default})


def validaratividade(request,id, action):

    user_check_var = uviews.user_check(request=request, user_profile=[Coordenador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    atividade=Atividade.objects.get(id=id)
    if action==0:
        nviews.enviar_notificacao_automatica(request,"rejeitarAtividade",id) #Enviar Notificacao Automatica !!!!!!
        atividade.estado='Recusada'
    if action==1:
        nviews.enviar_notificacao_automatica(request,"confirmarAtividade",id) #Enviar Notificacao Automatica !!!!!!
        atividade.estado='Aceite'
    atividade.save()
    return redirect('atividades:atividadesUOrganica')


def verresumo(request,id):

    user_check_var = uviews.user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    if atividade.exists():  
        atividade= Atividade.objects.get(id=id)
        nsub= 0
        if atividade.estado == "nsub":
            nsub= 1
        print(nsub)
        if request.method == "POST":
            if 'anterior' in request.POST:
                return redirect('atividades:inserirSessao', id)
        sessions_activity= Sessao.objects.filter(atividadeid=atividade)
        return render(request=request, 
                    template_name="atividades/resumo.html",  context={"atividade": atividade, "sessions_activity": sessions_activity, "nsub": nsub} )
    else:
        return redirect('atividades:minhasAtividades')


def confirmarResumo(request,id):
    user_check_var = uviews.user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    if atividade.exists():  
        atividade= Atividade.objects.get(id=id)
        if atividade.estado == "nsub":
            atividade.estado= "Pendente"
            atividade.save()
        print(atividade.id)
        nviews.enviar_notificacao_automatica(request,"validarAtividades",atividade.id) #Enviar Notificacao Automatica !!!!!!!!!!!!!!!!!!!!!!!!!
        return redirect("atividades:minhasAtividades")
    else:
        return redirect('atividades:minhasAtividades')

#---------------------End David
    
