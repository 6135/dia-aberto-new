from django.test import Client, SimpleTestCase, TestCase
from utilizadores.models import Administrador, Participante
from inscricoes.models import Escola, Inscricao
from configuracao.models import Campus, Diaaberto
from django.utils.datetime_safe import datetime
from django.urls import reverse
from inscricoes.views import InscricaoWizard
from configuracao.tests.test_models import create_open_day
from utilizadores.tests.test_models import create_Administrador_0, create_Colaborador_0, create_Coordenador_0, create_Participante_0, create_ProfessorUniversitario_0, create_Utilizador_0


class TestInscricaoWizardView(TestCase):
    """ Teste suite da view "CriarInscricao" da app "inscricoes" """

    def assertNaoTemPermissoes(self, response):
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para aceder a esta página!')

    def test_CriarInscricao_semLogin(self):
        create_open_day()
        response = self.client.get(reverse('inscricoes:criar-inscricao'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_CriarInscricao_naoParticipante(self):
        create_open_day()
        for utilizador in [create_Utilizador_0(), create_Coordenador_0(), create_ProfessorUniversitario_0(), create_Colaborador_0(), create_Administrador_0()]:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:criar-inscricao'), follow=True)
            self.assertNaoTemPermissoes(response)
            self.client.logout()

    def test_CriarInscricao_naoHaDiaAberto(self):
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Ainda não é permitido criar inscrições')

    def test_CriarInscricao_ok(self):
        create_open_day()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(reverse('inscricoes:criar-inscricao'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_info.html')
        self.assertIsNotNone(response.context['wizard'])
