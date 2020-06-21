from django.shortcuts import get_object_or_404, render
from inscricoes.models import Inscricao, Inscricaosessao, Responsavel
from inscricoes.utils import add_vagas_sessao, enviar_mail_confirmacao_inscricao, init_form, nao_tem_permissoes, render_pdf, save_form, update_context, update_post
from django_filters import filters
import django_filters
from atividades.models import Atividade, Sessao
from atividades.serializers import AtividadeSerializer
from atividades.filters import AtividadeFilter
from inscricoes.forms import AlmocoForm, InfoForm, InscricaoForm, ResponsavelForm, SessoesForm, TransporteForm
from utilizadores.models import Administrador, Coordenador, Participante
from utilizadores.views import user_check
from django.http import HttpResponseRedirect
from django.urls import reverse
from inscricoes.tables import InscricoesTable
from inscricoes.filters import InscricaoFilter
from django.db.models import Exists, OuterRef


def InscricaoPDF(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    erro_permissoes = nao_tem_permissoes(request, inscricao)
    if erro_permissoes:
        return erro_permissoes
    ano = inscricao.diaaberto.ano
    context = {
        'request': request,
        'inscricao': inscricao,
        'ano': ano,
    }
    return render_pdf("inscricoes/pdf.html", context, f"dia_aberto_ualg_{ano}.pdf")


class AtividadesAPIView(ListAPIView):

    class AtividadesPagination(pagination.PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100

    search_fields = '__all__'
    ordering_fields = '__all__'
    ordering = 'nome'
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter, django_filters.DjangoFilterBackend)
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer
    pagination_class = AtividadesPagination
    filterset_class = AtividadeFilter


class InscricaoWizard(SessionWizardView):
    form_list = [
        ('info', InfoForm),
        ('responsaveis', ResponsavelForm),
        ('escola', InscricaoForm),
        ('transporte', TransporteForm),
        ('almoco', AlmocoForm),
        ('sessoes', SessoesForm),
    ]

    def dispatch(self, request, *args, **kwargs):
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
                inscricao_sessao = Inscricaosessao(sessao=Sessao.objects.get(
                    pk=sessaoid), nparticipantes=sessoes[sessaoid], inscricao=inscricao)
                add_vagas_sessao(sessaoid, -sessoes[sessaoid])
                inscricao_sessao.save()
        responsaveis.inscricao = inscricao
        responsaveis.save()
        if almoco is not None:
            almoco.inscricao = inscricao
            almoco.save()
        enviar_mail_confirmacao_inscricao(inscricao.pk)
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
        inscricao = get_object_or_404(Inscricao, pk=pk)
        erro_permissoes = nao_tem_permissoes(request, inscricao)
        if erro_permissoes:
            return erro_permissoes
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
        inscricao = get_object_or_404(Inscricao, pk=pk)
        erro_permissoes = nao_tem_permissoes(request, inscricao)
        if erro_permissoes:
            return erro_permissoes
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
    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(
            request=request, user_profile=[Participante])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Inscricao.objects.filter(participante__user_ptr=self.request.user)


class InscricoesDepartamento(ConsultarInscricoes):
    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[
            Coordenador, Participante, Administrador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        coordenador = Coordenador.objects.get(user_ptr=self.request.user)
        self.queryset = Inscricao.objects.filter(
            Exists(Inscricaosessao.objects.filter(
                inscricao=OuterRef('pk'),
                sessao__atividadeid__professoruniversitarioutilizadorid__departamento=coordenador.departamento
            ))
        )
        return super().dispatch(request, *args, **kwargs)


def ApagarInscricao(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    erro_permissoes = nao_tem_permissoes(request, inscricao)
    if erro_permissoes:
        return erro_permissoes
    inscricaosessao_set = inscricao.inscricaosessao_set.all()
    for inscricaosessao in inscricaosessao_set:
        sessaoid = inscricaosessao.sessao.id
        nparticipantes = inscricaosessao.nparticipantes
        add_vagas_sessao(sessaoid, nparticipantes)
    inscricao.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
