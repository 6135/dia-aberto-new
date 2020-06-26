from django.test import Client, TestCase
from utilizadores.models import Administrador, Participante
from inscricoes.models import Escola, Inscricao
from configuracao.models import Campus, Diaaberto
from django.utils.datetime_safe import datetime
from django.urls import reverse
from configuracao.tests.test_models import create_open_day
from utilizadores.tests.test_models import create_Administrador_0, create_Colaborador_0, create_Coordenador_0, create_Participante_0, create_Participante_1, create_ProfessorUniversitario_0, create_Utilizador_0
from unittest import mock
import pytz
from unittest.mock import Mock
from inscricoes.tests.test_models import create_Inscricao_0, create_Inscricao_1
from dia_aberto.views import error404


class TestInscricaoPDFView(TestCase):
    """ Teste suite da view "InscricaoPDF" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_InscricaoPDF_GET_inscricaoNaoExiste(self):
        """ Teste de método GET quando inscrição não existe """
        self.client.force_login(create_Coordenador_0())
        pk = 2
        while Inscricao.objects.filter(pk=pk).count() > 0:
            pk += 1
        response = self.client.get(
            reverse('inscricoes:inscricao-pdf', kwargs={'pk': pk}))
        self.assertRedirects(response, reverse(
            'utilizadores:mensagem', args=[404]))

    def test_InscricaoPDF_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:inscricao-pdf', kwargs={'pk': self.inscricao.pk}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_InscricaoPDF_GET_naoParticipanteCoordenadorAdministradorColaborador(self):
        """ Teste de método GET sem ser participante """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:inscricao-pdf', kwargs={'pk': self.inscricao.pk}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_InscricaoPDF_GET_inscricaoDeOutroParticipante(self):
        """ Teste de método GET logado como outro Participante """
        self.client.force_login(create_Participante_1())
        response = self.client.get(
            reverse('inscricoes:inscricao-pdf', kwargs={'pk': self.inscricao.pk}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para aceder a esta página!')

    def test_InscricaoPDF_GET_ok(self):
        """ Teste de método GET sucesso """
        create_open_day()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:inscricao-pdf', kwargs={'pk': self.inscricao.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inscricoes/pdf.html')
        self.assertIsNotNone(response.context['request'])
        self.assertEquals(response.context['inscricao'], self.inscricao)
        self.assertEquals(
            response.context['ano'], self.inscricao.diaaberto.ano)


class TestAtividadesAPIView(TestCase):
    """ Teste suite da view "AtividadesAPI" da app "inscricoes" """

    def test_AtividadesAPI_GET_vazia(self):
        """ Teste de método GET sem login """
        response = self.client.get(reverse('inscricoes:api-atividades'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        })


class TestCriarInscricaoView(TestCase):
    """ Teste suite da view "CriarInscricao" da app "inscricoes" """

    def test_CriarInscricao_GET_semLogin(self):
        """ Teste de método GET sem login """
        create_open_day()
        response = self.client.get(reverse('inscricoes:criar-inscricao'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_CriarInscricao_GET_naoParticipante(self):
        """ Teste de método GET sem ser participante """
        create_open_day()
        utilizadores = [create_Utilizador_0(),
                        create_Coordenador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0(),
                        create_Administrador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(reverse('inscricoes:criar-inscricao'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_CriarInscricao_GET_naoHaDiaAberto(self):
        """ Teste de método GET sem ser participante """
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Ainda não é permitido criar inscrições')

    @mock.patch('inscricoes.views.datetime', Mock(now=Mock(return_value=datetime(2020, 1, 1, 9, 30, tzinfo=pytz.UTC))))
    def test_CriarInscricao_GET_antesDoPeriodoDeInscricoes(self):
        """ Teste de método GET antes do período de inscricões """
        diaaberto = create_open_day()
        diaaberto.datainscricaoatividadesinicio = datetime(
            2021, 1, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.datainscricaoatividadesfim = datetime(
            2021, 3, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.save()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], f'Período de abertura das inscrições: 01/01/2021 até 01/03/2021')

    @mock.patch('inscricoes.views.datetime', Mock(now=Mock(return_value=datetime(2021, 4, 1, 9, 30, tzinfo=pytz.UTC))))
    def test_CriarInscricao_GET_depoisDoPeriodoDeInscricoes(self):
        """ Teste de método GET depois do período de inscricões """
        diaaberto = create_open_day()
        diaaberto.datainscricaoatividadesinicio = datetime(
            2021, 1, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.datainscricaoatividadesfim = datetime(
            2021, 3, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.save()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], f'Período de abertura das inscrições: 01/01/2021 até 01/03/2021')

    def test_CriarInscricao_GET_ok(self):
        """ Teste de método GET sucesso """
        create_open_day()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(reverse('inscricoes:criar-inscricao'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_info.html')
        self.assertIsNotNone(response.context['wizard'])

    def test_CriarInscricao_POST_semLogin(self):
        """ Teste de método POST sem login """
        create_open_day()
        response = self.client.post(reverse('inscricoes:criar-inscricao'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_CriarInscricao_POST_naoParticipante(self):
        """ Teste de método POST sem ser participante """
        create_open_day()
        utilizadores = [create_Utilizador_0(),
                        create_Coordenador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0(),
                        create_Administrador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.post(reverse('inscricoes:criar-inscricao'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_CriarInscricao_POST_naoHaDiaAberto(self):
        """ Teste de método POST sem ser participante """
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Ainda não é permitido criar inscrições')

    @mock.patch('inscricoes.views.datetime', Mock(now=Mock(return_value=datetime(2020, 1, 1, 9, 30, tzinfo=pytz.UTC))))
    def test_CriarInscricao_POST_antesDoPeriodoDeInscricoes(self):
        """ Teste de método POST antes do período de inscricões """
        diaaberto = create_open_day()
        diaaberto.datainscricaoatividadesinicio = datetime(
            2021, 1, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.datainscricaoatividadesfim = datetime(
            2021, 3, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.save()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], f'Período de abertura das inscrições: 01/01/2021 até 01/03/2021')

    @mock.patch('inscricoes.views.datetime', Mock(now=Mock(return_value=datetime(2021, 4, 1, 9, 30, tzinfo=pytz.UTC))))
    def test_CriarInscricao_POST_depoisDoPeriodoDeInscricoes(self):
        """ Teste de método POST depois do período de inscricões """
        diaaberto = create_open_day()
        diaaberto.datainscricaoatividadesinicio = datetime(
            2021, 1, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.datainscricaoatividadesfim = datetime(
            2021, 3, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.save()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], f'Período de abertura das inscrições: 01/01/2021 até 01/03/2021')

    def test_CriarInscricao_POST_ok(self):
        """ Teste de método POST sucesso """
        create_open_day()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(reverse('inscricoes:criar-inscricao'), {
                                    'criar_inscricao-current_step': ['info'], 'info-individual': ['True']}, follow=True)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_responsaveis.html')
        self.assertIsNotNone(response.context['wizard'])


class TestConsultarInscricaoView(TestCase):
    """ Teste suite da view "ConsultarInscricao" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_ConsultarInscricao_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ConsultarInscricao_GET_inscricaoNaoExiste(self):
        """ Teste de método GET quando inscrição não existe """
        self.client.force_login(self.inscricao.participante)
        pk = 2
        while Inscricao.objects.filter(pk=pk).count() > 0:
            pk += 1
        response = self.client.get(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': pk}))
        self.assertRedirects(response, reverse(
            'utilizadores:mensagem', args=[404]))

    def test_ConsultarInscricao_GET_naoParticipanteCoordenadorAdministrador(self):
        """ Teste de método GET sem ser participante, coordenador ou administrador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_ConsultarInscricao_GET_outroParticipante(self):
        """ Teste de método GET sendo outro participante """
        self.client.force_login(create_Participante_1())
        response = self.client.get(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')

    def test_ConsultarInscricao_GET_ok(self):
        """ Teste de método GET sucesso """
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_responsaveis.html')
            
    def test_ConsultarInscricao_POST_semLogin(self):
        """ Teste de método POST sem login """
        response = self.client.post(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ConsultarInscricao_POST_inscricaoNaoExiste(self):
        """ Teste de método POST quando inscrição não existe """
        self.client.force_login(self.inscricao.participante)
        pk = 2
        while Inscricao.objects.filter(pk=pk).count() > 0:
            pk += 1
        response = self.client.post(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': pk}))
        self.assertRedirects(response, reverse(
            'utilizadores:mensagem', args=[404]))

    def test_ConsultarInscricao_POST_naoParticipanteCoordenadorAdministrador(self):
        """ Teste de método POST sem ser participante, coordenador ou administrador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.post(
                reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_ConsultarInscricao_POST_outroParticipante(self):
        """ Teste de método POST sendo outro participante """
        self.client.force_login(create_Participante_1())
        response = self.client.post(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')

    def test_ConsultarInscricao_POST_ok(self):
        """ Teste de método POST sucesso """
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_responsaveis.html')

class TestMinhasInscricoesView(TestCase):
    """ Teste suite da view "MinhasInscricoes" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_MinhasInscricoes_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-participante'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_MinhasInscricoes_GET_naoParticipante(self):
        """ Teste de método GET sem ser participante """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Administrador_0(),
                        create_Coordenador_0(),
                        create_Colaborador_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:consultar-inscricoes-participante'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_MinhasInscricoes_GET_ok(self):
        """ Teste de método GET sucesso """
        self.client.force_login(self.inscricao.participante)
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-participante'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inscricoes/consultar_inscricoes_participante.html')
        self.assertIsNotNone(response.context['table'])

class TestInscricoesDepartamentoView(TestCase):
    """ Teste suite da view "InscricoesDepartamento" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_InscricoesDepartamento_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-coordenador'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_InscricoesDepartamento_GET_naoCoordenador(self):
        """ Teste de método GET sem ser coordenador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Administrador_0(),
                        create_Participante_0(),
                        create_Colaborador_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:consultar-inscricoes-coordenador'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_InscricoesDepartamento_GET_ok(self):
        """ Teste de método GET sucesso """
        self.client.force_login(create_Coordenador_0())
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-coordenador'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inscricoes/consultar_inscricoes_coordenador.html')
        self.assertIsNotNone(response.context['table'])


class TestInscricoesAdminView(TestCase):
    """ Teste suite da view "InscricoesAdmin" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_InscricoesAdmin_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-admin'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_InscricoesAdmin_GET_naoAdministrador(self):
        """ Teste de método GET sem ser administrador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Coordenador_0(),
                        create_Participante_0(),
                        create_Colaborador_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:consultar-inscricoes-admin'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_InscricoesAdmin_GET_ok(self):
        """ Teste de método GET sucesso """
        self.client.force_login(create_Administrador_0())
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-admin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inscricoes/consultar_inscricoes_admin.html')
        self.assertIsNotNone(response.context['table'])


class TestApagarInscricaoView(TestCase):
    """ Teste suite da view "ApagarInscricao" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_ApagarInscricao_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.post(
            reverse('inscricoes:apagar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ApagarInscricao_GET_inscricaoNaoExiste(self):
        """ Teste de método GET quando inscrição não existe """
        self.client.force_login(self.inscricao.participante)
        pk = 2
        while Inscricao.objects.filter(pk=pk).count() > 0:
            pk += 1
        response = self.client.get(
            reverse('inscricoes:apagar-inscricao', kwargs={'pk': pk}))
        self.assertRedirects(response, reverse(
            'utilizadores:mensagem', args=[404]))

    def test_ApagarInscricao_GET_naoParticipanteCoordenadorAdministrador(self):
        """ Teste de método GET sem ser participante, coordenador ou administrador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:apagar-inscricao', kwargs={'pk': self.inscricao.pk}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_ApagarInscricao_GET_outroParticipante(self):
        """ Teste de método GET sendo outro participante """
        self.client.force_login(create_Participante_1())
        response = self.client.get(
            reverse('inscricoes:apagar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')

    def test_ApagarInscricao_GET_ok(self):
        """ Teste de método GET sucesso """
        inscricao = create_Inscricao_1()
        self.client.force_login(create_Administrador_0())
        response = self.client.get(
            reverse('inscricoes:apagar-inscricao', kwargs={'pk': inscricao.pk}))
        assert not Inscricao.objects.filter(pk=inscricao.pk).exists()