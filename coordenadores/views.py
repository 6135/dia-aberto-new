from django.shortcuts import render, redirect  
from .models import *
from .forms import *
from inscricoes.models import *
from configuracao.models import Horario
from utilizadores.models import ProfessorUniversitario, Coordenador
from configuracao.models import Diaaberto, Horario, Campus, Edificio, Espaco
from django.http import HttpResponseRedirect
from datetime import datetime, date,timezone,time
from _datetime import timedelta
from django.db.models import Q
from coordenadores.forms import *
from notificacoes import views
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters.views import FilterView
from coordenadores.tables import TarefaTable
from coordenadores.filters import TarefaFilter
from utilizadores.views import user_check
#def adicionartarefa(request, id = None):
#    tarefa = Tarefa()
#    if id is not None:
#        tarefa=Tarefa.objects.get(id=id)
#        temp = "alterar" #Enviar Notificacao Automatica !!!!!!
#    else: #Enviar Notificacao Automatica !!!!!!
#        temp = "atribuir" #Enviar Notificacao Automatica !!!!!!    
#    form_tarefa=TarefaForm(user=request.user.id,instance=tarefa)
#    if request.method == 'POST':
#        form_tarefa=TarefaForm(user=request.user.id,data=request.POST,instance=tarefa)
#        print(form_tarefa.errors)
#        if form_tarefa.is_valid():
#            tarefa_saved=form_tarefa.save()
#            if request.POST['tipo'] == 'tarefaAuxiliar':        
#                auxiliar_form = TarefaAuxiliarForm(request.POST,instance=TarefaAuxiliar(tarefaid=tarefa_saved))
#                print(auxiliar_form.errors)
#                if auxiliar_form.is_valid():
#                    auxiliar_form.save()
#                    #if temp == "atribuir": #Enviar Notificacao Automatica !!!!!!
#                    #    views.enviar_notificacao_automatica(request,"tarefaAtribuida",id) #Enviar Notificacao Automatica !!!!!!
#                    #elif temp == "alterar": #Enviar Notificacao Automatica !!!!!!
#                    #    views.enviar_notificacao_automatica(request,"tarefaAlterada",id) #Enviar Notificacao Automatica !!!!!!
#                    return redirect('coordenadores:consultarTarefa') 
#            elif request.POST['tipo'] == 'tarefaOutra': 
#                outra_form = TarefaOutraForm(request.POST,instance=TarefaOutra(tarefaid=tarefa_saved)) 
#                print(outra_form.errors)
#                if outra_form.is_valid():
#                    outra_form.save()
#                    #if temp == "atribuir" and tarefa_saved.colab: #Enviar Notificacao Automatica !!!!!!
#                    #    views.enviar_notificacao_automatica(request,"tarefaAtribuida",id) #Enviar Notificacao Automatica !!!!!!
#                    #elif temp == "alterar" and tarefa_saved.colab: #Enviar Notificacao Automatica !!!!!!
#                    #    views.enviar_notificacao_automatica(request,"tarefaAlterada",id) #Enviar Notificacao Automatica !!!!!!
#                    return redirect('coordenadores:consultarTarefa') 
#            elif request.POST['tipo'] == 'tarefaAcompanhar': 
#                acompanhar_form = TarefaAcompanharForm(request.POST,instance=TarefaAcompanhar(tarefaid=tarefa_saved)) 
#                
#                if acompanhar_form.is_valid():
#                    acompanhar_form.save()
#                    #if temp == "atribuir": #Enviar Notificacao Automatica !!!!!!
#                    #    views.enviar_notificacao_automatica(request,"tarefaAtribuida",id) #Enviar Notificacao Automatica !!!!!!
#                    #elif temp == "alterar": #Enviar Notificacao Automatica !!!!!!
#                    #    views.enviar_notificacao_automatica(request,"tarefaAlterada",id) #Enviar Notificacao Automatica !!!!!!
#                    return redirect('coordenadores:consultarTarefa') 
#                print(acompanhar_form.errors)
#            else:
#                tarefa_saved.delete()      
#    return render(request=request,
#                template_name='coordenadores/criarTarefa.html',
#                context={'formTarefa':form_tarefa}
#    )
#

def adicionartarefa(request,id=None):
    if id:
        tarefa = Tarefa.objects.get(id=id)
    else:
        tarefa = None
    if request.method == 'POST':
        if request.POST['tipo']=='tarefaAuxiliar':
            form = TarefaAuxiliarForm(request.POST)
            if form.is_valid():
                coord = Coordenador.objects.get(id=request.user.id)
                form.save(user=coord,id=id)
                return redirect('coordenadores:consultarTarefa')
        if request.POST['tipo']=='tarefaAcompanhar':
            form = TarefaAcompanharForm(request.POST)
            if form.is_valid():
                coord = Coordenador.objects.get(id=request.user.id)
                print(id)
                form.save(user=coord,id=id)
                return redirect('coordenadores:consultarTarefa')
        if request.POST['tipo']=='tarefaOutra':
            form = TarefaOutraForm(request.POST)
            if form.is_valid():
                coord = Coordenador.objects.get(id=request.user.id)
                form.save(user=coord,id=id)
                return redirect('coordenadores:consultarTarefa')
    
    return render(request = request,template_name='coordenadores/criarTarefa.html',context={'tarefa':tarefa})



def tipoTarefa(request):
    template =''
    form = ''
    if request.method == 'POST':
        tipo = request.POST['tipo']
        if tipo == 'tarefaAuxiliar':
            template = 'coordenadores/tarefaAuxiliar.html'
            if request.POST.get('id'):
                tarefa = TarefaAuxiliar.objects.get(tarefaid=int(request.POST['id']))
                form = TarefaAuxiliarForm()
            else:
                form = TarefaAuxiliarForm()       
        elif tipo == 'tarefaAcompanhar':
            template = 'coordenadores/tarefaAcompanhar.html'
            if request.POST.get('id'):
                tarefa = TarefaAcompanhar.objects.get(tarefaid=int(request.POST['id']))
                form = TarefaAcompanharForm(initial={'grupo':tarefa.inscricao.id,'dia':tarefa.tarefaid.dia})
            else:
                 form = TarefaAcompanharForm()           
        elif tipo == 'tarefaOutra':
            template = 'coordenadores/tarefaOutra.html'
            if request.POST.get('id'):
                tarefa = TarefaOutra.objects.get(tarefaid=int(request.POST['id']))
                form = TarefaOutraForm(initial={'dia':tarefa.tarefaid.dia,'horario':tarefa.tarefaid.horario,'descricao':tarefa.descricao})      
            else:
                  form = TarefaOutraForm()
            
    return render(request=request,template_name=template,context={'form':form})

def diasAtividade(request):
    
    dias=[]
    if request.POST['atividadeid'] != '':
        if 'tarefa' in request.POST and request.POST['tarefa']!='':
            tarefa = Tarefa.objects.get(id=request.POST['tarefa'])
            default={
                'key': tarefa.dia,
                'value': tarefa.dia
            }
        else:
            default = {
                'key': '',
                'value': 'Escolha o dia'
            }
    atividadeid = request.POST.get('atividadeid')
    atividade = Atividade.objects.get(id=atividadeid)   
    dias = atividade.get_dias()  
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':dias, 'default': default}
            )

def sessoesAtividade(request):
    dia = request.POST['dia']
    atividade= request.POST['atividadeid']
    sessoes = Sessao.tarefas_get_sessoes(atividade=atividade,dia=dia)
    default = {
        'key': '',
        'value': 'Escolha a sessão'
    }
    options = [{
                    'key':	str(sessao.id),
                    'value':	str(sessao.horarioid.inicio) + ' até ' + str(sessao.horarioid.fim)
                } for sessao in sessoes
            ]
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options': options, 'default': default}
            )

def colaboradores(request):
    coordenador = Coordenador.objects.get(id = request.user.id)
    colabs = Colaborador.objects.filter(faculdade = coordenador.faculdade,utilizador_ptr_id__valido=True)
    default = {
        'key': '',
        'value': 'Escolha o colaborador'
    }
    
    options = [{
                    'key':	str(colab.utilizador_ptr_id),
                    'value':	str(colab)
                } for colab in colabs
            ]

    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':options, 'default': default}
            )

def grupoInfo(request):
    info = Inscricao.objects.get(id=request.POST['grupo_id'])
    #reponsavel = Responsavel.objects.get(inscricao=request.POST['grupo_id'])
    return render(request=request,
                template_name='coordenadores/grupoInfo.html',
                context={'info': info}
            )

def diasGrupo(request):
    dias=[]
    if request.POST['grupo_id'] != '':
        if 'tarefa' in request.POST and request.POST.get('tarefa')!='':
            tarefa = Tarefa.objects.get(id=request.POST.get('tarefa'))
            
            default={
                'key': str(tarefa.dia),
                'value': str(tarefa.dia)
            }
        else:
            default = {
                'key': '',
                'value': 'Escolha o dia'
            }
        inscricaoid = request.POST.get('grupo_id')
        inscricao = Inscricao.objects.get(id=inscricaoid)
        dias = inscricao.get_dias()
        print(default)
        print(dias)
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':dias, 'default': default}
            )

def horarioGrupo(request):
    default = {
        'key': '',
        'value': 'Escolha o horário'
    }
    horario=[]
    if request.POST['dia'] != '' and request.POST['grupo_id'] != '':
        if 'tarefa' in request.POST and request.POST.get('tarefa')!='':
            tarefa = Tarefa.objects.get(id=request.POST.get('tarefa'))
            default={
                'key': str(tarefa.dia),
                'value': str(tarefa.dia)
            }
        else:
            default = {
                'key': '',
                'value': 'Escolha o dia'
            }
        inscricaoid = request.POST.get('grupo_id')
        inscricao = Inscricao.objects.get(id=inscricaoid)
        horario = inscricao.get_horarios(request.POST['dia'])
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':horario, 'default': default}
            )

def locaisOrigem(request):
    default = {
        'key': '',
        'value': 'Escolha o local de encontro'
    }
    if request.POST['sessao_id']:
        origens = []
        inscricaoid = request.POST.get('grupo_id')
        inscricao = Inscricao.objects.get(id=inscricaoid)
        origens =  inscricao.get_origem(request.POST['dia'],request.POST['sessao_id'])
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':origens, 'default': default}
            )  

def locaisDestino(request):
    default = {
        'key': '',
        'value': 'Escolha o local de destino'
    }
    if request.method == 'POST':
        destinos = []
        inscricaoid = request.POST.get('grupo_id')
        inscricao = Inscricao.objects.get(id=inscricaoid)
        destinos =  inscricao.get_destino(request.POST['dia'],request.POST['sessao_id'])
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':destinos, 'default': default}
            )  

class ConsultarTarefas(SingleTableMixin, FilterView):
    table_class = TarefaTable
    template_name = 'coordenadores/consultartarefa.html'
    filterset_class = TarefaFilter
    table_pagination = {
		'per_page': 10
	}

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[Coordenador])
        if not user_check_var.get('exists'): return user_check_var.get('render')
        self.user = user_check_var.get('firstProfile')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Tarefa.objects.filter(coord=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        context["colabs"] = list(map(lambda x: (x.id, x.full_name), Colaborador.objects.filter(faculdade = self.user.faculdade,utilizador_ptr_id__valido=True)))
        context[self.get_context_table_name(table)] = table
        return context

def eliminartarefa(request,id):
    tarefa = ''
    user_check_var = user_check(request=request, user_profile=[Coordenador])
    if not user_check_var.get('exists'): return user_check_var.get('render')
    if Tarefa.objects.filter(id=id).exists():
        tarefa = Tarefa.objects.get(id=id)
    if tarefa.coord.id == user_check_var.get('firstProfile').id:
        tarefa.delete()
        return redirect('coordenadores:consultarTarefa')
    return redirect('coordenadores:consultarTarefa')



#def consultartarefa(request):
#    tarefas=Tarefa.objects.all()
#    tarefasacompanhar= TarefaAcompanhar.objects.all()
#    tarefasauxiliar= TarefaAuxiliar.objects.all()
#    colaboradores= Colaborador.objects.all()
#    tarefasoutra= TarefaOutra.objects.all()
#    if request.method == 'POST' or request.GET.get('searchTarefa'):
#        form_tarefa=TarefaForm(request.POST)
#        today=datetime.now(timezone.utc)
#        diaAberto=Diaaberto.objects.filter(datadiaabertofim__gte=today).first()
#        filterForm=tarefaFilterForm(request.POST)
#        nome=str(request.POST.get('searchTarefa'))
#        tarefas=tarefas.filter(Q(nome__icontains=nome) | Q(colab__utilizadorid__nome__icontains=nome))
#        tipo=str(request.POST.get('tipo'))
#        if tipo != ' ' and tipo != 'None':
#            tarefas=tarefas.filter(tipo=tipo)
#        if request.POST.get('Concluida') or request.POST.get('naoConcluida')  or request.POST.get('naoAtribuida'):
#            filter=filters(request)
#            tarefas=tarefas.filter(Q(estado=filter[0]) | Q(estado=filter[1]) | Q(estado=filter[2]))
#    else:
#        form_tarefa= TarefaForm(user=request.user.id)
#        filterForm=tarefaFilterForm()
#
#    return render(request=request,
#			    template_name="coordenadores/consultartarefa.html",
#                context={"tarefas": tarefas,"tarefasauxiliar": tarefasauxiliar,"tarefasacompanhar": tarefasacompanhar,"tarefasoutra": tarefasoutra,"filter":filterForm, "formtarefa":form_tarefa, "colaboradores": colaboradores}
#            )
#
##def atribuircolaborador(request,tarefa):
#    tarefa= Tarefa.objects.get(id=tarefa)
#    colaborador= Colaborador.objects.get(utilizadorid=request.POST['colab'])
#    tarefa.estado= "naoConcluida"
#    tarefa.colab= colaborador
#    tarefa.save()
#    views.enviar_notificacao_automatica(request,"tarefaAtribuida",tarefa) #Enviar Notificacao Automatica !!!!!!
#    return redirect('coordenadores:consultarTarefa'
