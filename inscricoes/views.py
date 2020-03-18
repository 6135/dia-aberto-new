from django.shortcuts import render
from django.core.exceptions import ValidationError
from .forms import InscricaoIndividualForm, InscricaoColetivaForm, EscolaForm
from utilizadores.forms import ParticipanteForm
from django.http.request import HttpRequest
from django.views.generic.edit import CreateView
from .models import Inscricaoindividual

def CriarInscricaoIndividual(request: HttpRequest):
    if request.method == 'POST':
        participanteForm = ParticipanteForm(request.POST)
        inscricaoForm = InscricaoIndividualForm(request.POST)
        if participanteForm.is_valid() and inscricaoForm.is_valid():
            participante = participanteForm.save()
            inscricao = inscricaoForm.save(commit=False)
            inscricao.participante = participante
            inscricao.save()
    else:
        participanteForm = ParticipanteForm()
        inscricaoForm = InscricaoIndividualForm()
    return render(request, 'inscricoes/criar_inscricao_individual.html', {
        'participante_form': participanteForm,
        'inscricao_form': inscricaoForm,
    })

def CriarInscricaoColetiva(request : HttpRequest):
    if request.method == 'POST':
        participanteForm = ParticipanteForm(request.POST)
        inscricaoForm = InscricaoColetivaForm(request.POST)
        escolaForm = EscolaForm(request.POST)
        if participanteForm.is_valid() and  escolaForm.is_valid() and inscricaoForm.is_valid():
            participante = participanteForm.save()
            escola = escolaForm.save()
            inscricao = inscricaoForm.save(commit = False)
            inscricao.participante = participante
            inscricao.escola = escola
            inscricao.save()
    else:
        participanteForm = ParticipanteForm()
        escolaForm = EscolaForm()
        inscricaoForm = InscricaoColetivaForm()
    return render(request, 'inscricoes/criar_inscricao_coletiva.html',{
        'participante_form': participanteForm,
        'escola_form': escolaForm,
        'inscricao_form': inscricaoForm,
    })


