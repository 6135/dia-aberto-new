from django.shortcuts import render, redirect  
from .forms import AtividadeForm , MateriaisForm, atividadesFilterForm, CampusForm
from .models import *
from configuracao.models import Horario
from .models import Atividade, Sessao, Tema, Materiais
from coordenadores.models import Coordenador
from utilizadores.models import ProfessorUniversitario
from configuracao.models import Diaaberto, Horario, Campus, Edificio, Espaco
from django.http import HttpResponseRedirect
from datetime import datetime, date,timezone
from _datetime import timedelta
from django.db.models import Q
from django.core import serializers
from django.forms.models import modelformset_factory
from django.forms.widgets import Select



#-------------Diogo----------------------
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
    atividades=Atividade.objects.all()
    sessoes=Sessao.objects.all()
    materiais= Materiais.objects.all()
    conflito2= []
    for atividade1 in atividades:
        for atividade2 in atividades:
            if atividade1.id!=atividade2.id:
                if atividade1.espacoid== atividade2.espacoid:
                    sessao1= Sessao.objects.filter(atividadeid=atividade1)
                    sessao2= Sessao.objects.filter(atividadeid=atividade2)
                    sessao1horario= []
                    sessao2horario= []
                    for s1 in sessao1:
                        sessao1horario.append(s1.horarioid) 
                    for s2 in sessao2:
                        sessao2horario.append(s2.horarioid)
                    for horario1 in sessao1horario:
                        if horario1 in sessao2horario:
                            C1=Conflito(atividade1,atividade2)
                            conflito2.append(C1)
    for c in conflito2:
        print(c.atividade1)                
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
            context={"atividades": atividades,"conflitos":conflito2,"sessoes":sessoes,"materiais": materiais,"filter":filterForm})

def alterarAtividade(request,id):
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
        if activity_object_form.is_valid():
                #-------Guardar as mudancas a atividade em si------
                activity_object_formed = activity_object_form.save(commit=False)  
                activity_object_formed.estado = "Pendente"
                activity_object_formed.dataalteracao = datetime.now()
                activity_object_formed.save()
                materiais_object_form.save()
                return redirect('inserirSessao',id)          
    return render(request=request,
                    template_name='atividades/proporAtividadeAtividade.html',
                    context={'form': activity_object_form, 'espaco':espaco,'espacos':espacos, "edificios": edificios, "campus":campus, "materiais":materiais_object_form}
                    )

def eliminarAtividade(request,id):
    Atividade.objects.get(id=id).delete() #Dupla (sessao,atividade)
    return HttpResponseRedirect('/minhasatividades')


def eliminarSessao(request,id):
    atividadeid=Sessao.objects.get(id=id).atividadeid.id
    Sessao.objects.get(id=id).delete()
    return redirect('inserirSessao',atividadeid)
#-----------------EndDiogo------------------


#----------------- original

#def proporatividade(request):
#    today= datetime.now(timezone.utc) 
#    diaaberto=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)
#    if request.method == "POST":
#        print(diaaberto.id)
#        activity_object_form = AtividadeForm(request.POST)
#        campus=Campus.objects.all()
#        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizador=5),
#                             professoruniversitarioutilizadorid = ProfessorUniversitario.objects.get(utilizadorid=2),
#                             estado = "Pendente", diaabertoid = diaaberto,espacoid= Espaco.objects.get(id=request.POST['espacoid']),
#                             tema=Tema.objects.get(id=request.POST['tema']))
#        activity_object_form = AtividadeForm(request.POST, instance=new_form)
#        material_object_form= MateriaisForm(request.POST)
#        if activity_object_form.is_valid():
#            #activity_object_form.save()
#            idAtividade= Atividade.objects.all().order_by('-id').first()
#            #new_material= Materiais(atividadeid=idAtividade)
#            #material_object_form= MateriaisForm(request.POST, instance= new_material)
#            #material_object_form.save()
#            #return redirect('inserirSessao', idAtividade.id)
#            
#    else:
#        material_object_form= MateriaisForm() 
#        activity_object_form= AtividadeForm()
#    return render(request,'atividades/proporAtividadeAtividade.html',{'form': activity_object_form,'campus': Campus.objects.all(), "espaco": -1, "materiais": material_object_form})


#-------------------- versao sem reload

def proporatividade(request, id = None):
    today= datetime.now(timezone.utc) 
    diaaberto=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)
    dias_diaaberto = diaaberto.days_as_array()

    sessoes = ""
    SessaoFormSet = SessaoFormset()
    sessao_form_set = SessaoFormSet(queryset=Sessao.objects.none())
    material_object_form= MateriaisForm() 
    activity_object_form= AtividadeForm()

    if id is not None:
        pass

    if request.method == "POST":

        espaco= Espaco.objects.get(id=request.POST['espacoid'])
        activity_object_form = AtividadeForm(request.POST)
        campus=Campus.objects.all()
        activity_object_form = AtividadeForm(request.POST)
        material_object_form= MateriaisForm(request.POST)

        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizador=5),
                            professoruniversitarioutilizadorid = ProfessorUniversitario.objects.get(utilizadorid=2),
                            estado = "Pendente", diaabertoid = diaaberto,espacoid= espaco,
                            tema=Tema.objects.get(id=request.POST['tema'])
                        )
        activity_object_form = AtividadeForm(request.POST, instance=new_form)
        sessao_form_set = SessaoFormSet(request.POST)

        if activity_object_form.is_valid() and sessao_form_set.is_valid():  
            atividade_object = activity_object_form.save()  
            new_material= Materiais(atividadeid=atividade_object)
            material_object_form= MateriaisForm(request.POST, instance= new_material)
            material_object_form.is_valid()
            material_object_form.save()

            instances = sessao_form_set.save(commit=False)

            for instance in instances:
                instance.vagas=atividade_object.participantesmaximo
                instance.ninscritos = 0
                instance.atividadeid = atividade_object
                instance.save()
            for instance in sessao_form_set.deleted_objects:
                instance.delete()

            return redirect('minhasAtividades')
        else:
            for dict in sessao_form_set.errors:
                for error in dict.values:
                    print(error)

    return render(request= request,
                template_name='atividades/testAtividade.html',
                context={'form': activity_object_form,
                        'campus': Campus.objects.all(),
                        "materiais": material_object_form,
                        'horarios': "" , 
                        'sessions_activity':sessoes, 
                        'dias': dias_diaaberto, 
                        'formset': sessao_form_set
                        #"id":-1,
                        }
                    )

def SessaoFormset(extra = 0, minVal = 1):
    formSets = modelformset_factory(model=Sessao, exclude = ['id','ninscritos','vagas','atividadeid'],widgets={
			'dia': Select(attrs={'class': 'input dia-sessao'}),
			'horarioid': Select(attrs={'class': 'input horario-sessao'}),
		}, extra = extra, min_num = minVal, can_delete=True)
    return formSets

#---------------original 


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

def verhorarios(request):
    horarios = []
    default = {
        'key': '',
        'value': 'Escolha um horario'
    }
    options = [{
        'key': str(horario.id),
        'value': str(horario),
    } for horario in Horario.objects.exclude(inicio="12:00", fim="14:00")]

    return render(request=request, 
                template_name="configuracao/dropdown.html", 
                context={"options": options,    "default": default})


def validaratividade(request,id, action):
    atividade=Atividade.objects.get(id=id)
    if action==0:
        atividade.estado='Recusada'
    if action==1:
        atividade.estado='Aceite'
    atividade.save()
    return redirect('minhasAtividades')

#---------------------End David
    
