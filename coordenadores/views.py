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
from coordenadores.forms import tarefaFilterForm

# Create your views here.
def adicionartarefa(request):
    form=TarefaForm()
    if request.method == 'POST':
        print(request.POST['tipo'])
        if request.POST['tipo']=='Atividade':
            tarefa_form=tarefaAtividade(request)
            tarefa_form.save()
            return redirect('consultarTarefa')      
    return render(request=request,template_name='coordenadores/criarTarefa.html',context={'form':form})

def tarefaAtividade(request):
    atividade=Atividade.objects.get(id=request.POST['atividades'])
    nome='Auxiliar na atividade '+atividade.nome
    sessaoid=Sessao.objects.get(id=int(request.POST['sessoes']))
    colaborador=Colaborador.objects.get(utilizadorid=request.POST['colaborador'])
    return Tarefa(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=5),concluida=0,nome=nome,sessaoid=sessaoid,colaboradorutilizadorid=colaborador)

def sessoesAtividade(request):
    dia = request.POST['dia']
    sessoes= Sessao.objects.filter(dia=dia)
    return render(request,template_name='coordenadores/sessoesDropdown.html',context={'sessoes':sessoes})

def colaboradoresAtividade(request):
    sessao = request.POST['sessao']
    tarefas= Tarefa.objects.filter(sessaoid=sessao)
    if tarefas.count()>0:
        colaboradores=[]
        for tarefa in tarefas:
            colaboradores.append(Colaborador.objects.filter(~Q(utilizadorid=tarefa.colaboradorutilizadorid.utilizadorid)))
    else:
        print('hello')
        colaboradores=Colaborador.objects.all()
    return render(request,template_name='coordenadores/colaboradoresDropdown.html',context={'colaboradores':colaboradores})

def diasAtividade(request):
    atividadeid = request.POST['atividadeid']
    sessoes= Sessao.objects.filter(atividadeid=atividadeid)
    dias=[]
    for sessao in sessoes:
        if sessao.dia not in dias:
            dias.append(sessao.dia)
    return render(request,template_name='coordenadores/diasDropdown.html',context={'dias':dias})

def filters(request):
    filters=[]
    if request.POST.get('Realizada'):
        filters.append('Realizada')
    else:
        filters.append('')

    if request.POST.get('PorRealizar'):
        filters.append('PorRealizar')
    else:
        filters.append('')
    return filters

def consultartarefa(request):
    tarefas=Tarefa.objects.all()
    if request.method == 'POST' or request.GET.get('searchTarefa'):
        today=datetime.now(timezone.utc)
        diaAberto=Diaaberto.objects.filter(datadiaabertofim__gte=today).first()
        filterForm=tarefaFilterForm(request.POST)
        nome=str(request.POST.get('searchTarefa'))
        tarefas=tarefas.filter(nome__icontains=nome)
        tipo=str(request.POST.get('tipo'))
        departamento=str(request.POST.get('departamentos'))
        if tipo != ' ' and tipo != 'None':
            tarefas=tarefas.filter(tipo=tipo)
        if departamento != 'None' and departamento > '-1':
            print('departamento')
            tarefas=tarefas.filter(sessaoid__atividadeid__professoruniversitarioutilizadorid__departamento__id=departamento)
        if request.POST.get('Concluida') or request.POST.get('naoConcluida'):
            print('estado')
            filter=filters(request)
            tarefas=tarefas.filter(Q(concluida=1) | Q(concluida=0))
    else:
        filterForm=tarefaFilterForm()

    return render(request=request,
			template_name="coordenadores/consultartarefa.html",
            context={"tarefas": tarefas,"filter":filterForm})
