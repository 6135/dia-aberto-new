from django.shortcuts import render, redirect  
from .models import *
from .forms import *
from configuracao.models import Horario
from coordenadores.models import Coordenador
from utilizadores.models import ProfessorUniversitario
from configuracao.models import Diaaberto, Horario, Campus, Edificio, Espaco
from django.http import HttpResponseRedirect
from datetime import datetime, date,timezone
from _datetime import timedelta
from django.db.models import Q
from coordenadores.forms import *

# Create your views here.
def adicionartarefa(request, id = None):
    tarefa = Tarefa()
    if id is not None:
        tarefa=Tarefa.objects.get(id=id)
    form_tarefa=TarefaForm(instance=tarefa)
    if request.method == 'POST':
        form_tarefa=TarefaForm(request.POST, instance=tarefa)
        if form_tarefa.is_valid():
            form_tarefa.save()
            if request.POST['tipo'] == 'tarefaAuxiliar':
                auxiliar_form = TarefaAuxiliarForm(request.POST,initial={'tarefaid':form_tarefa.instance})
                if auxiliar_form.is_valid():
                    print('hello')
                    auxiliar_form.save()
                    return redirect('consultarTarefa') 
                else:
                    form_tarefa.instance.delete()      
    return render(request=request,
                template_name='coordenadores/criarTarefa.html',
                context={'formTarefa':form_tarefa}
            )

def tarefaAuxiliar(request,id):
    atividade=Atividade.objects.get(id=request.POST['atividades'])
    nome='Auxiliar na atividade ' + str(atividade.nome)
    sessaoid=Sessao.objects.get(id=int(request.POST['sessoes']))
    colaborador=Colaborador.objects.get(utilizadorid=request.POST['colaborador'])
    return TarefaAuxiliar(tarefaid=id,sessaoid=sessaoid)

def tipoTarefa(request):
    if request.method == 'POST':
        tipo = request.POST['tipo']
        if tipo == 'tarefaAuxiliar':
            form = TarefaAuxiliarForm()
            template = 'coordenadores/tarefaAuxiliar.html'
        elif tipo == 'tarefaAcompanhar':
            form = TarefaAcompanharForm()
        elif tipo == 'tarefaOutra':   
            form = TarefaOutraForm()
            template = 'coordenadores/tarefaOutra.html'
    return render(request=request,template_name=template,context={'form':form})

def sessoesAtividade(request):
    dia = request.POST['dia']
    sessoes = Sessao.objects.filter(dia=dia)
    default = {
        'key': '',
        'value': '--------'
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

def colaboradoresAtividade(request):
    sessao = request.POST['sessao']
    colabs = Colaborador.objects.all()
    default = {
        'key': '',
        'value': '--------'
    }
    
    options = [{
                    'key':	str(colab.utilizadorid.id),
                    'value':	str(colab)
                } for colab in colabs
            ]

    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':options, 'default': default}
            )

def diasAtividade(request):
    atividadeid = request.POST['atividadeid']
    sessoes= Sessao.objects.filter(atividadeid=atividadeid)
    default = {
        'key': '',
        'value': '--------'
    }
    dias=[]
    for sessao in sessoes:
        if sessao.dia not in dias:
            dias.append({'key':str(sessao.dia), 'value':sessao.dia})
            
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':dias, 'default': default}
            )

def filters(request):
    filters=[]
    if request.POST.get('Concluida'):
        filters.append('Concluida')
    else:
        filters.append('')

    if request.POST.get('naoConcluida'):
        filters.append('naoConcluida')
    else:
        filters.append('')

    if request.POST.get('naoAtribuida'):
        filters.append('naoAtribuida')
    else:
        filters.append('')
    return filters

def consultartarefa(request):
    tarefas=Tarefa.objects.all()
    tarefasacompanhar= TarefaAcompanhar.objects.all()
    tarefasauxiliar= TarefaAuxiliar.objects.all()
    colaboradores= Colaborador.objects.all()
    tarefasoutra= TarefaOutra.objects.all()
    if request.method == 'POST' or request.GET.get('searchTarefa'):
        form_tarefa=TarefaForm(request.POST)
        today=datetime.now(timezone.utc)
        diaAberto=Diaaberto.objects.filter(datadiaabertofim__gte=today).first()
        filterForm=tarefaFilterForm(request.POST)
        nome=str(request.POST.get('searchTarefa'))
        tarefas=tarefas.filter(Q(nome__icontains=nome) | Q(colab__utilizadorid__nome__icontains=nome))
        tipo=str(request.POST.get('tipo'))
        if tipo != ' ' and tipo != 'None':
            tarefas=tarefas.filter(tipo=tipo)
        if request.POST.get('Concluida') or request.POST.get('Nao Concluida')  or request.POST.get('Nao Concluida'):
            print('estado')
            filter=filters(request)
            tarefas=tarefas.filter(Q(estado=filter[0]) | Q(estado=filter[1]) | Q(estado=filter[2]))
    else:
        form_tarefa= TarefaForm()
        filterForm=tarefaFilterForm()

    return render(request=request,
			    template_name="coordenadores/consultartarefa.html",
                context={"tarefas": tarefas,"tarefasauxiliar": tarefasauxiliar,"tarefasacompanhar": tarefasacompanhar,"tarefasoutra": tarefasoutra,"filter":filterForm, "formtarefa":form_tarefa, "colaboradores": colaboradores}
            )

def eliminartarefa(request,id):
    Tarefa.objects.get(id=id).delete()
    return redirect('consultarTarefa')


def atribuircolaborador(request,tarefa):
    tarefa= Tarefa.objects.get(id=tarefa)
    form_tarefa=TarefaForm(instance=tarefa)
    print(form_tarefa)
    if request.method == 'POST':
        form_tarefa=TarefaForm(request.POST, instance=tarefa)
        print("Hello")
        if form_tarefa.is_valid():
            form_tarefa.save()
    print(request.POST)
    form_tarefa.save()
    return redirect('consultarTarefa')

