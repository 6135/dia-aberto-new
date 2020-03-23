from django.shortcuts import render, redirect  
from .forms import AtividadeForm , SessaoForm
from .models import Atividade, Espaco, Sessao, Atividadesessao
from coordenadores.models import Coordenador
from utilizadores.models import Professoruniversitario  
from configuracao.models import Diaaberto, Horario
from django.http import HttpResponseRedirect
from atividades.forms import MateriaisForm


#-------------Diogo----------------------

def proporatividade(request):
	return render(request=request,
				  template_name="atividades/proporatividade.html",)

def minhasatividades(request):
	return render(request=request,
				template_name="atividades/listaAtividades.html",
                context={"atividades": Atividade.objects.all()})

def alterarAtividade(request,id):
    change_activity= Atividade.objects.get(id=id)   
    
    if request.method == 'POST':
        change_activity.estado='Pendente'
        changed_form=AtividadeForm(request.POST,instance=change_activity)
        if changed_form.is_valid():
            changed_form.save() 
            return HttpResponseRedirect('/thanks/')
        else:
            return HttpResponseRedirect('/didntwork/')
    else:
        return render(request=request,
                    template_name='atividades/proporatividade.html',
                    context={'atividade': change_activity}
                    )
#-----------------EndDiogo------------------


#-----------------------David--------------------
def inseriratividade(request):  
    if request.method == "POST":
        form_Sessao= SessaoForm(request.POST)
        form_Materiais= MateriaisForm(request.POST)
        new_form = Atividade(coordenadorutilizadorid = Coordenador.objects.get(utilizadorid=1),
                             professoruniversitarioutilizadorid = Professoruniversitario.objects.get(utilizadorid=2),
                             estado = "Pendente", diaabertoid = Diaaberto.objects.all().order_by('-id').first())
        formAtividade = AtividadeForm(request.POST, instance=new_form)

        if formAtividade.is_valid() and form_Sessao.is_valid() and form_Materiais.is_valid():
            new_form.save()  
            sessao = form_Sessao.save(commit= False)
            materiais = form_Materiais.save(commit= False)
            materiais.atividadeid = Atividade.objects.all().order_by('-id').first()
            materiais.save()
            sessao.vagas= sessao.participantesmaximo
            sessao.ninscritos= 0
            sessao.espacoid= Espaco.objects.get(id=request.POST.__getitem__('idespaco'))
            sessao.horarioid = Horario.objects.get(id=request.POST.__getitem__('idhorario'))
            sessao.save()
            return HttpResponseRedirect('/thanks/')
        else:
            return render(request, 'atividades/inseriratividade.html',{'atividade': formAtividade , 'sessao': form_Sessao,'horario':  Horario.objects.all(), 'espaco': Espaco.objects.all(),'materiais': form_Materiais})
    else:  
        formAtividade = AtividadeForm()
        form_Sessao= SessaoForm()
        form_Materiais= MateriaisForm() 
    return render(request,'atividades/inseriratividade.html',{'atividade': formAtividade,'sessao': form_Sessao,'horario':  Horario.objects.all(), 'espaco': Espaco.objects.all, 'materiais': form_Materiais})  
#---------------------End David
    