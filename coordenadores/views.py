from django.shortcuts import render, redirect  
from atividades.forms import AtividadeForm , MateriaisForm
from .models import *
from .forms import *
from configuracao.models import Horario
from atividades.models import Atividade, Sessao, Tema
from coordenadores.models import Coordenador
from utilizadores.models import Professoruniversitario
from configuracao.models import Diaaberto, Horario, Campus, Edificio, Espaco
from django.http import HttpResponseRedirect
from datetime import datetime, date,timezone
from _datetime import timedelta
from django.db.models import Q
from coordenadores.forms import tarefaFilterForm




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

# Create your views here.
def consultartarefa(request):
    atividades=Atividade.objects.all()
    sessoes=Sessao.objects.all()
    if request.method == 'POST' or request.GET.get('searchAtividade'):
        today=datetime.now(timezone.utc)
        diaAberto=Diaaberto.objects.filter(datadiaabertofim__gte=today).first()
        filterForm=tarefaFilterForm(request.POST)
        nome=str(request.POST.get('searchAtividade'))
        atividades=atividades.filter(nome__icontains=nome)
        tipo=str(request.POST.get('tipo'))
        departamento=str(request.POST.get('departamentos'))
        if tipo != ' ' and tipo != 'None':
            atividades=atividades.filter(tipo=tipo)
        if departamento != 'None' and departamento > '-1':
            print('departamento')
            atividades=atividades.filter(professoruniversitarioutilizadorid__departamento__id=departamento)
            filter=filters(request)
            atividades=atividades.filter(Q(estado=filter[0]) | Q(estado=filter[1]) | Q(estado=filter[2]))
        if request.POST.get('diaAbertoAtual'):
            atividades=atividades.filter(diaabertoid=diaAberto)    
    else:
        filterForm=tarefaFilterForm()

    return render(request=request,
			template_name="coordenadores/consultartarefa.html",
            context={"atividades": atividades,"sessoes":sessoes,"filter":filterForm})
