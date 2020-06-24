from django.test import Client, SimpleTestCase, TestCase
from utilizadores.models import Administrador, Participante
from inscricoes.models import Escola, Inscricao
from configuracao.models import Diaaberto
from django.utils.datetime_safe import datetime
import pytz
from django.urls import reverse
from inscricoes.views import InscricaoWizard

def create_open_day():
    return Diaaberto.objects.create(
        precoalunos = 2,
        precoprofessores = 2,
        enderecopaginaweb = 'web.com',
        descricao = 'Dia Aberto',
        emaildiaaberto = 'web@web.com',
        ano = '2020',
        datadiaabertoinicio = datetime(1970,1,1,9,30,tzinfo=pytz.UTC),
        datadiaabertofim = datetime(2040,1,2,9,30,tzinfo=pytz.UTC),
        datainscricaoatividadesinicio = datetime(1970,1,1,9,30,tzinfo=pytz.UTC),
        datainscricaoatividadesfim = datetime(2040,1,2,9,30,tzinfo=pytz.UTC),
        datapropostasatividadesincio = datetime(1970,1,1,9,30,tzinfo=pytz.UTC),
        dataporpostaatividadesfim = datetime(2040,1,2,9,30,tzinfo=pytz.UTC),
        administradorutilizadorid = None,
        escalasessoes = '00:30',
    )

class CriarInscricaoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participante = Participante.objects.create_user('inesvalentim')
        cls.diaaberto = create_open_day()
        cls.diaaberto.save()

    def test_CriarInscricao_Sucesso(self):
        self.client.force_login(self.participante)
        response = self.client.get(reverse('inscricoes:criar-inscricao'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inscricoes/inscricao_wizard_info.html')
        self.assertIsNotNone(response.context['wizard'])