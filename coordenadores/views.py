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
def adicionartarefa(request):
    form_tarefa=TarefaForm()
    if request.method == 'POST':
        form_tarefa=TarefaForm(request.POST)
        print(form_tarefa)
        if form_tarefa.is_valid():
            tarefa.save()
            if request.POST['tipo'] == 'Atividade':
                auxiliar_form = TarefaAuxiliarForm(request.POST,initial={'tarefaid':tarefa})
                if auxiliar_form.is_valid():
                   auxiliar_form.save()
                else:
                    tarefa.delete() 
            return redirect('consultarTarefa')      
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
            template='coordenadores/tarefaAuxiliar.html'
        elif tipo == 'tarefaAcompanhar':
            form = TarefaAcompanharForm()
        elif tipo == 'tarefaOutra':   
            form = TarefaOutraForm()
    return render(request=request,
                template_name=template,
                context={'form':form}
            )

def sessoesAtividade(request):
    dia = request.POST['dia']
    sessoes= Sessao.objects.filter(dia=dia)
    return render(request=request,
                template_name='coordenadores/sessoesDropdown.html',
                context={'sessoes':sessoes}
            )

def colaboradoresAtividade(request):
    sessao = request.POST['sessao']
    colaboradores=Colaborador.objects.all()
    return render(request=request,
                template_name='coordenadores/colaboradoresDropdown.html',
                context={'colaboradores':colaboradores}
            )

def diasAtividade(request):
    atividadeid = request.POST['atividadeid']
    sessoes= Sessao.objects.filter(atividadeid=atividadeid)
    dias=[]
    for sessao in sessoes:
        if sessao.dia not in dias:
            dias.append(sessao.dia)
    return render(request=request,
                template_name='coordenadores/diasDropdown.html',
                context={'dias':dias}
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
    tarefasoutra= TarefaOutra.objects.all()
    if request.method == 'POST' or request.GET.get('searchTarefa'):
        today=datetime.now(timezone.utc)
        diaAberto=Diaaberto.objects.filter(datadiaabertofim__gte=today).first()
        filterForm=tarefaFilterForm(request.POST)
        nome=str(request.POST.get('searchTarefa'))
        tarefas=tarefas.filter(Q(nome__icontains=nome) | Q(colaboradorutilizadorid__utilizadorid__nome__icontains=nome))
        tipo=str(request.POST.get('tipo'))
        if tipo != ' ' and tipo != 'None':
            tarefas=tarefas.filter(tipo=tipo)
        if request.POST.get('Concluida') or request.POST.get('Nao Concluida')  or request.POST.get('Nao Concluida'):
            print('estado')
            filter=filters(request)
            tarefas=tarefas.filter(Q(estado=filter[0]) | Q(estado=filter[1]) | Q(estado=filter[2]))
    else:
        filterForm=tarefaFilterForm()

    return render(request=request,
			    template_name="coordenadores/consultartarefa.html",
                context={"tarefas": tarefas,"tarefasauxiliar": tarefasauxiliar,"tarefasacompanhar": tarefasacompanhar,"tarefasoutra": tarefasoutra,"filter":filterForm}
            )
