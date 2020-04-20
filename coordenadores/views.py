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
    
    return render(request=request,template_name='coordenadores/criarTarefa.html')



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
