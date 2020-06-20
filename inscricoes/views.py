from configuracao.models import Campus, Departamento, Diaaberto, Menu, Prato, Unidadeorganica
from atividades.models import Atividade, Sessao
import django_filters.rest_framework as djangofilters
from rest_framework import filters, pagination
from rest_framework.generics import ListCreateAPIView
from inscricoes.models import Escola, Responsavel
from utilizadores.models import Participante
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
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
from django.db import transaction
from django.db.models import F
from _datetime import date
import pytz
from django.views import View
from django.urls import reverse
from datetime import datetime
from django.utils import timezone as tz
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from dia_aberto import settings
from django.core.mail import BadHeaderError, send_mail
import os


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def render_pdf(template_path, context={}, filename="file.pdf"):
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponseBadRequest()
    return response


def InscricaoPDF(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    ano = inscricao.diaaberto.ano
    context = {
        'inscricao': inscricao,
        'ano': ano,
    }
    return render_pdf("inscricoes/pdf.html", context, f"dia_aberto_ualg_{ano}.pdf")


class AtividadesAPIView(ListCreateAPIView):

    class AtividadeFilter(djangofilters.FilterSet):
        nome = djangofilters.CharFilter(
            field_name="nome", lookup_expr='icontains')
        campus_id = djangofilters.NumberFilter(
            field_name="espacoid__edificio__campus__id")
        unidade_organica_id = djangofilters.NumberFilter(
            field_name="espacoid__edificio__campus__id")
        # TODO: Adicionar filtros
        # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
        # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

        class Meta:
            model = Atividade
            fields = '__all__'

    class AtividadesPagination(pagination.PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100

    search_fields = '__all__'
    ordering_fields = '__all__'
    ordering = 'nome'
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter, djangofilters.DjangoFilterBackend)
    queryset = Atividade.objects.all()
    serializer_class = serializers.AtividadeSerializer
    pagination_class = AtividadesPagination
    filterset_class = AtividadeFilter


def add_vagas_sessao(sessaoid, vagas):
    with transaction.atomic():
        sessao = Sessao.objects.select_for_update().get(pk=sessaoid)
        sessao.vagas = F('vagas') + vagas
        sessao.save()


def init_form(step, inscricao, POST=None):
    form = None
    if step == 'responsaveis':
        responsavel = inscricao.responsavel_set.first()
        form = forms.ResponsavelForm(POST, instance=responsavel)
    elif step == 'escola':
        form = forms.InscricaoForm(POST,
                                   instance=inscricao,
                                   initial={
                                       'nome_escola': inscricao.escola.nome,
                                       'local': inscricao.escola.local,
                                       'dia': inscricao.dia.strftime("%d/%m/%Y"),
                                   })
    elif step == 'transporte':
        initial = {
            'meio': inscricao.meio_transporte,
            'entrecampi': inscricao.entrecampi,
        }
        if initial['meio'] != 'outro':
            initial.update({
                'hora_chegada': inscricao.hora_chegada.strftime("%H:%M"),
                'local_chegada': inscricao.local_chegada,
            })
        form = forms.TransporteForm(POST,
                                    initial=initial)
    elif step == 'almoco':
        form = forms.AlmocoForm(POST,
                                instance=inscricao.inscricaoprato_set.first(),
                                initial={
                                    'nalunos': inscricao.nalunos,
                                    'nresponsaveis': 1,
                                    'individual': inscricao.individual,
                                })
    elif step == 'sessoes':
        inscricoes_sessao = inscricao.inscricaosessao_set.all()
        sessoes = {}
        sessoes_info = []
        for inscricao_sessao in inscricoes_sessao:
            sessao = inscricao_sessao.sessao
            sessoes[sessao.id] = inscricao_sessao.nparticipantes
            sessoes_info.append({
                'atividade': {'nome': sessao.atividadeid.nome, 'sala': sessao.atividadeid.get_sala_str()},
                'sessao': {
                    'id': sessao.id,
                    'vagas': sessao.vagas + inscricao_sessao.nparticipantes,
                    'horario': {
                        'inicio': sessao.horarioid.inicio.strftime("%H:%M:%S"),
                        'fim': sessao.horarioid.fim.strftime("%H:%M:%S"),
                    },
                },
            })
        sessoes = json.dumps(sessoes)
        sessoes_info = json.dumps(sessoes_info)
        form = forms.SessoesForm(POST,
                                 initial={
                                     'sessoes': sessoes,
                                     'sessoes_info': sessoes_info,
                                     'nalunos': inscricao.nalunos,
                                 })
    return form


def update_context(context, step, wizard=None, inscricao=None):
    if step == 'escola':
        prox_diaaberto = Diaaberto.current()
        context.update({
            'escolas': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Escola.objects.all()))),
            'inicio': prox_diaaberto.datadiaabertoinicio.strftime("%d/%m/%Y"),
            'fim': prox_diaaberto.datadiaabertofim.strftime("%d/%m/%Y"),
        })
    elif step == 'almoco':
        diaaberto = Diaaberto.current()
        campi = Campus.objects.all()
        pratos_info = {}
        for tipoid, tipo in Prato.tipos:
            pratos_info[tipo] = {}
            for campus in campi:
                pratos_info[tipo][campus] = []
                menu_filter = Menu.objects.filter(
                    diaaberto=diaaberto, campus=campus)
                if menu_filter.exists():
                    menu = menu_filter.first()
                    for prato in menu.prato_set.filter(tipo=tipoid):
                        pratos_info[tipo][campus].append(prato.__str__())
        campi_str = list(map(lambda x: x.nome, Campus.objects.all()))
        context.update({
            'precoalunos': '%.2f' % diaaberto.precoalunos,
            'precoprofessores': '%.2f' % diaaberto.precoprofessores,
            'campi': campi_str,
            'pratos_info': pratos_info,
            'nalunos': wizard.get_cleaned_data_for_step('escola')['nalunos'] if wizard else inscricao.nalunos,
            'nresponsaveis': 1,
        })
    elif step == 'sessoes':
        context.update({
            'campus': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Campus.objects.all()))),
            'unidades_organicas': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Unidadeorganica.objects.all()))),
            'departamentos': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Departamento.objects.all()))),
            'tipos': json.dumps(list(map(lambda x: x[0], Atividade.tipos))),
            'nalunos': wizard.get_cleaned_data_for_step('escola')['nalunos'] if wizard else inscricao.nalunos,
        })
    elif step == 'submissao':
        context.clear()
        context.update({
            'inscricao': inscricao,
        })


def update_post(step, POST, wizard=None, inscricao=None):
    mutable = POST._mutable
    POST._mutable = True
    prefix = f"{step}-" if wizard else ''
    if step == 'escola':
        try:
            dia = tz.make_aware(datetime.strptime(
                POST[f'{prefix}dia'], "%d/%m/%Y"))
            diaaberto = Diaaberto.objects.filter(
                datadiaabertoinicio__lte=dia.replace(hour=23), datadiaabertofim__gte=dia.replace(hour=0)).first()
            if diaaberto:
                POST[f'{prefix}diaaberto'] = diaaberto.id
        except:
            pass
        POST[f'{prefix}individual'] = wizard.get_cleaned_data_for_step('info')[
            'individual'] if wizard else inscricao.individual
    elif step == 'almoco':
        POST[f'{prefix}nalunos'] = wizard.get_cleaned_data_for_step('escola')[
            'nalunos'] if wizard else inscricao.nalunos
        POST[f'{prefix}nresponsaveis'] = 1
        POST[f'{prefix}individual'] = wizard.get_cleaned_data_for_step('info')[
            'individual'] if wizard else inscricao.individual
    elif step == 'sessoes':
        POST[f'{prefix}nalunos'] = wizard.get_cleaned_data_for_step('escola')[
            'nalunos'] if wizard else inscricao.nalunos
    POST._mutable = mutable


def save_form(step, form, inscricao):
    if step == 'almoco':
        almoco = form.save(commit=False)
        if almoco is not None:
            almoco.inscricao = inscricao
            almoco.save()
        else:
            inscricaoalmoco = inscricao.inscricaoalmoco_set.first()
            if inscricaoalmoco:
                inscricaoalmoco.delete()
    if step == 'transporte':
        inscricao.meio_transporte = form.cleaned_data['meio']
        outro = form.cleaned_data['meio'] == 'outro'
        inscricao.hora_chegada = form.cleaned_data['hora_chegada'] if not outro else None
        inscricao.local_chegada = form.cleaned_data['local_chegada'] if not outro else None
        inscricao.entrecampi = form.cleaned_data['entrecampi']
        inscricao.save()
    elif step == 'sessoes':
        for inscricao_sessao in inscricao.inscricaosessao_set.all():
            inscricao_sessao.delete()
        sessoes = form.cleaned_data['sessoes']
        for sessaoid in sessoes:
            if sessoes[sessaoid] > 0:
                inscricao_sessao = models.Inscricaosessao(sessao=Sessao.objects.get(
                    pk=sessaoid), nparticipantes=sessoes[sessaoid], inscricao=inscricao)
                add_vagas_sessao(sessaoid, -sessoes[sessaoid])
                inscricao_sessao.save()
    else:
        form.save()


class InscricaoWizard(SessionWizardView):
    form_list = [
        ('info', forms.InfoForm),
        ('responsaveis', forms.ResponsavelForm),
        ('escola', forms.InscricaoForm),
        ('transporte', forms.TransporteForm),
        ('almoco', forms.AlmocoForm),
        ('sessoes', forms.SessoesForm),
    ]

    def dispatch(self, request, *args, **kwargs):
        from utilizadores.views import user_check
        _user_check = user_check(request, [Participante])
        if _user_check['exists']:
            participante = _user_check['firstProfile']
            self.instance_dict = {
                'responsaveis': Responsavel(nome=f"{participante.first_name} {participante.last_name}", email=participante.email, tel=participante.contacto)
            }
        else:
            return _user_check['render']
        return super(InscricaoWizard, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        update_context(context, self.steps.current, self)
        if self.steps.current != 'info':
            context.update({
                'individual': self.get_cleaned_data_for_step('info')['individual']
            })
        visited = []
        for step in self.form_list:
            cleaned_data = self.get_cleaned_data_for_step(step)
            if cleaned_data:
                visited.append(True)
            else:
                visited.append(False)
        context.update({
            'visited': visited
        })
        return context

    def get_template_names(self):
        return [f'inscricoes/inscricao_wizard_{self.steps.current}.html']

    def post(self, *args, **kwargs):
        # Envia a informação extra necessária para o formulário atual, após preenchê-lo.
        # Necessário para algumas validações especiais de backend, como verificar o número de alunos
        # inscritos para verificar inscritos nos almoços e nas sessões.
        update_post(self.steps.current, self.request.POST, self)
        print(self.request.POST)
        return super(InscricaoWizard, self).post(*args, **kwargs)

    def done(self, form_list, form_dict, **kwargs):
        # Guardar na Base de Dados
        # TODO: Responsáveis
        responsaveis = form_dict['responsaveis'].save(commit=False)
        almoco = form_dict['almoco'].save(commit=False)
        inscricao = form_dict['escola'].save(commit=False)
        inscricao.participante = Participante.objects.filter(
            utilizador_ptr_id=self.request.user.id).first()
        inscricao.meio_transporte = form_dict['transporte'].cleaned_data['meio']
        if(form_dict['transporte'].cleaned_data['meio'] != 'outro'):
            inscricao.hora_chegada = form_dict['transporte'].cleaned_data['hora_chegada']
            inscricao.local_chegada = form_dict['transporte'].cleaned_data['local_chegada']
        inscricao.entrecampi = form_dict['transporte'].cleaned_data['entrecampi']
        inscricao.save()
        sessoes = form_dict['sessoes'].cleaned_data['sessoes']
        for sessaoid in sessoes:
            if sessoes[sessaoid] > 0:
                inscricao_sessao = models.Inscricaosessao(sessao=Sessao.objects.get(
                    pk=sessaoid), nparticipantes=sessoes[sessaoid], inscricao=inscricao)
                add_vagas_sessao(sessaoid, -sessoes[sessaoid])
                inscricao_sessao.save()
        responsaveis.inscricao = inscricao
        responsaveis.save()
        if almoco is not None:
            almoco.inscricao = inscricao
            almoco.save()
        # TODO: Construir PDF
        return render(self.request, 'inscricoes/consultar_inscricao_submissao.html', {
            'inscricao': inscricao,
        })


class ConsultarInscricao(View):
    template_prefix = 'inscricoes/consultar_inscricao'
    step_names = [
        'responsaveis',
        'escola',
        'transporte',
        'almoco',
        'sessoes',
        'submissao'
    ]

    def get(self, request, pk, step=0, alterar=False):
        context = {}
        inscricao = get_object_or_404(Inscricao, pk=pk)
        form = init_form(self.step_names[step], inscricao)
        context.update({'alterar': alterar,
                        'pk': pk,
                        'step': step,
                        'individual': inscricao.individual,
                        'form': form,
                        })
        update_context(context, self.step_names[step], inscricao=inscricao)
        return render(request, f"{self.template_prefix}_{self.step_names[step]}.html", context)

    def post(self, request, pk, step=0, alterar=False):
        context = {}
        inscricao = get_object_or_404(Inscricao, pk=pk)
        update_post(self.step_names[step], request.POST, inscricao=inscricao)
        form = init_form(self.step_names[step], inscricao, request.POST)
        inscricoessessao = inscricao.inscricaosessao_set.all()
        if self.step_names[step] == 'sessoes':
            for inscricao_sessao in inscricoessessao:
                add_vagas_sessao(inscricao_sessao.sessao.id,
                                 inscricao_sessao.nparticipantes)
        if form.is_valid():
            save_form(self.step_names[step], form, inscricao)
            return HttpResponseRedirect(reverse('inscricoes:consultar-inscricao', args=[pk, step]))
        if self.step_names[step] == 'sessoes':
            for inscricao_sessao in inscricoessessao:
                add_vagas_sessao(inscricao_sessao.sessao.id,
                                 -inscricao_sessao.nparticipantes)
        context.update({'alterar': alterar,
                        'pk': pk,
                        'step': step,
                        'individual': inscricao.individual,
                        'form': form,
                        })
        update_context(context, self.step_names[step], inscricao=inscricao)
        return render(request, f"{self.template_prefix}_{self.step_names[step]}.html", context)


class ConsultarInscricoes(SingleTableMixin, FilterView):
    table_class = InscricoesTable
    template_name = 'inscricoes/consultar_inscricoes.html'

    filterset_class = InscricaoFilter

    table_pagination = {
        'per_page': 8
    }


class MinhasInscricoes(ConsultarInscricoes):
    def get_queryset(self):
        return Inscricao.objects.filter(participante__user_ptr=self.request.user)


def ApagarInscricao(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    inscricaosessao_set = inscricao.inscricaosessao_set.all()
    for inscricaosessao in inscricaosessao_set:
        sessaoid = inscricaosessao.sessao.id
        nparticipantes = inscricaosessao.nparticipantes
        add_vagas_sessao(sessaoid, nparticipantes)
    inscricao.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def enviar_mail(request, id):
    user = Utilizador.objects.get(id=id)

    subject = 'Confirmação da Inscrição no Dia Aberto da Universidade do Algarve.'
    message = 'Exmo(a). '+user.first_name+'\n'
    message += 'A sua inscrição no Dia Aberto da Universidade do Algarve foi efectuada com sucesso!\n'
    message += 'Cumprimentos, Dia Aberto UAlg.'
    source = settings.EMAIL_HOST_USER
    recipient_list = [u.email, ]
    send_mail(subject, message, source, recipient_list)
