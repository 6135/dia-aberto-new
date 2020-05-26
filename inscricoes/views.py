from configuracao.models import Campus, Departamento, Unidadeorganica, Diaaberto
from atividades.models import Atividade, Sessao
import django_filters.rest_framework as djangofilters
from rest_framework import filters, pagination
from rest_framework.generics import ListCreateAPIView
from inscricoes.models import Escola, Responsavel
from utilizadores.models import Participante
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponse, JsonResponse
import json
from django.forms.formsets import formset_factory
from django.views.generic import CreateView, DetailView, TemplateView
from .models import Inscricao, Inscricaotransporte, Inscricaoprato, Escola
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ValidationError
from . import models
from . import forms
from . import serializers
from utilizadores.forms import ParticipanteForm
from django.http.request import HttpRequest
from django.views.generic import CreateView, DetailView, TemplateView, ListView
from atividades.models import Sessao, Atividade
from .tables import InscricoesTable, DepartamentoTable, DiaAbertoTable
from django_tables2 import RequestConfig, SingleTableView, MultiTableMixin, SingleTableMixin
from datetime import timezone
from .filters import InscricaoFilter
from django_filters.views import FilterView


class AtividadesAPIView(ListCreateAPIView):

    class AtividadeFilter(djangofilters.FilterSet):
        nome = djangofilters.CharFilter(
            field_name="nome", lookup_expr='icontains')
        campus_id = djangofilters.NumberFilter(
            field_name="espacoid__edificio__campus__id")
        unidade_organica_id = djangofilters.NumberFilter(
            field_name="espacoid__edificio__campus__id")
        # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
        # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

        class Meta:
            model = Atividade
            fields = '__all__'

    class AtividadesPagination(pagination.PageNumberPagination):
        page_size = 1000
        page_size_query_param = 'page_size'
        max_page_size = 10000

    search_fields = '__all__'
    ordering_fields = '__all__'
    ordering = 'nome'
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter, djangofilters.DjangoFilterBackend)
    queryset = Atividade.objects.all()
    serializer_class = serializers.AtividadeSerializer
    pagination_class = AtividadesPagination
    filterset_class = AtividadeFilter


class AlterarInscricaoWizard(SessionWizardView):

    form_list = [
        ('responsaveis', forms.ResponsavelForm),
        ('escola', forms.InscricaoForm),
        ('transporte', forms.TransporteForm),
        ('almoco', forms.TransporteForm),
        ('sessoes', forms.SessoesForm),
    ]

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        inscricao = Inscricao.objects.get(pk=pk)
        escola = inscricao.escola
        self.instance_dict = {
            'responsaveis': Responsavel.objects.get(inscricao__pk=pk)
        }
        self.initial_dict = {
            'escola': {
                'nome': escola.nome,
                'local': escola.local,
                'ano': inscricao.ano,
                'turma': "A",
                'nalunos': inscricao.nalunos,
                'areacientifica': inscricao.areacientifica,
            }
        }
        return super(AlterarInscricaoWizard, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return [f'inscricoes/inscricao_wizard_{self.steps.current}.html']

    def done(self, form_list, form_dict, **kwargs):
        # Save to DB
        print(form_dict)
        return HttpResponse('<h1>Done!</h1>')


class InscricaoWizard(SessionWizardView):
    form_list = [
        ('responsaveis', forms.ResponsavelForm),
        ('escola', forms.InscricaoForm),
        ('transporte', forms.TransporteForm),
        ('almoco', forms.AlmocoForm),
        ('sessoes', forms.SessoesForm),
        ('submissao', forms.SubmissaoForm),
    ]

    def dispatch(self, request, *args, **kwargs):
        participante = Participante.objects.filter(
            utilizador_ptr_id=request.user.id).first()
        self.instance_dict = {
            'responsaveis': Responsavel(nome=participante.username, email=participante.email, tel=participante.contacto)
        }
        return super(InscricaoWizard, self).dispatch(request, *args, **kwargs)

    def get_form_step_data(self, form):
        # print(f"DATA: {form.data}")
        # if(self.steps.current == 'sessoes'):
        #     print(f"SESSOES: {json.loads(form.data['sessoes-sessoes'])}")
        return form.data

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'escola':
            context.update({
                'escolas': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Escola.objects.all())))
            })
        elif self.steps.current == 'sessoes':
            context.update({
                'campus': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Campus.objects.all()))),
                'unidades_organicas': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Unidadeorganica.objects.all()))),
                'departamentos': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Departamento.objects.all()))),
                'tipos': json.dumps(list(map(lambda x: x[0], Atividade.tipos))),
                'nalunos': self.get_cleaned_data_for_step('escola')['nalunos'],
            })
        return context

    def get_template_names(self):
        return [f'inscricoes/inscricao_wizard_{self.steps.current}.html']

    def done(self, form_list, form_dict, **kwargs):
        # Save to DB
        sessoes = json.loads(form_dict['sessoes'].cleaned_data['sessoes'])
        responsaveis = form_dict['responsaveis'].save(commit=False)
        almoco = form_dict['almoco'].save(commit=False)
        inscricao = form_dict['escola'].save()
        for sessaoid in sessoes:
            if sessoes[sessaoid] > 0:
                inscricao_sessao = models.Inscricaosessao(sessao=Sessao.objects.get(
                    pk=sessaoid), nparticipantes=sessoes[sessaoid], inscricao=inscricao)
                inscricao_sessao.save()
        responsaveis.inscricao = inscricao
        almoco.inscricao = inscricao
        responsaveis.save()
        almoco.save()
        return render(self.request, 'inscricoes/mensagem.html', {
            'tipo': 'success',
            'm': "Inscrição bem sucedida!",
        })


class ConsultarInscricaoIndividual(TemplateView):

    template_name = 'inscricoes/consultar_inscricao.html'

    def get(self, request):
        form = InscricaoIndividualForm()
        inscricoes = Inscricaoindividual.objects.all()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InscricaoIndividualForm()
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.id = request.id
            inscricao.save()

        text = form.cleaned_data['post']
        form = InscricaoIndividualForm()
        return redirect('inscricao/criarinscricaoindividual')

        args = {'form': form, 'text': text}
        return render(request, "inscricoes/consultar_inscricao.html", args)


class ConsultarInscricoesListView(SingleTableMixin, FilterView):
    model = Inscricao
    table_class = InscricoesTable
    template_name = 'inscricoes/consultar_inscricoes.html'

    filterset_class = InscricaoFilter

    table_pagination = {
        'per_page': 10
    }
