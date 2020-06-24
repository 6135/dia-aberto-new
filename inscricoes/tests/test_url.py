from django.test import Client, SimpleTestCase, TestCase
from utilizadores.models import Administrador, Participante
from inscricoes.models import Escola, Inscricao
from configuracao.models import Diaaberto
from django.utils.datetime_safe import datetime
import pytz
from django.urls import reverse
from inscricoes.views import InscricaoPDF, InscricaoWizard
from utilizadores.tests.test_models import create_Participante_0


def create_open_day():
    return Diaaberto.objects.create(
        precoalunos=2,
        precoprofessores=2,
        enderecopaginaweb='web.com',
        descricao='Dia Aberto',
        emaildiaaberto='web@web.com',
        ano='2020',
        datadiaabertoinicio=datetime(1970, 1, 1, 9, 30, tzinfo=pytz.UTC),
        datadiaabertofim=datetime(2040, 1, 2, 9, 30, tzinfo=pytz.UTC),
        datainscricaoatividadesinicio=datetime(
            1970, 1, 1, 9, 30, tzinfo=pytz.UTC),
        datainscricaoatividadesfim=datetime(
            2040, 1, 2, 9, 30, tzinfo=pytz.UTC),
        datapropostasatividadesincio=datetime(
            1970, 1, 1, 9, 30, tzinfo=pytz.UTC),
        dataporpostaatividadesfim=datetime(2040, 1, 2, 9, 30, tzinfo=pytz.UTC),
        administradorutilizadorid=None,
        escalasessoes='00:30',
    )


class TestCriarInscricaoView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participante = create_Participante_0()
        cls.diaaberto = create_open_day()

    def setUp(self):
        self.client.force_login(self.participante)

    def test_url_criar_inscricao(self):
        response = self.client.get(reverse('inscricoes:criar-inscricao'))
        self.assertEqual(response.resolver_match.func.__name__,
                         InscricaoWizard.as_view().__name__)
        self.assertEqual(response.resolver_match.func, InscricaoPDF)
