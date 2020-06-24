from django.test import Client, SimpleTestCase, TestCase
from utilizadores.models import Administrador, Participante
from inscricoes.models import Escola, Inscricao
from django.urls import resolve
from configuracao.models import Diaaberto
from django.utils.datetime_safe import datetime


class InscricaoTest(TestCase):

    def setUp(self):
        self.participante = Participante(
            username="nuno_teste", password="andre123456", email="nunu_teste@teste.teste", contacto="+351912345678", valido="True")
        self.participante.save()
        self.escola = Escola(nome="Escola Secundária de Loulé", local="Loulé")
        self.escola.save()
        # self.diaaberto =

    def teste_criar_inscricao_individual_simples(self):
        # inscricao = Inscricao(individual=True, nalunos=1,
        #                       escola=self.escola, ano=12, participante=self.participante, dia="23/05/2021", diaaberto=self.diaaberto)
        pass

class InscricoesUrlsTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.participante = Participante.objects.create_user('inesvalentim')
        self.c.force_login(self.participante)
        admin = Administrador.objects.create_user('ivete')
        self.diaaberto = Diaaberto(precoalunos=1.60, precoprofessores=2.00, enderecopaginaweb="www.yo.yo", descricao="AH", emaildiaaberto="email@mail.mail", ano=2020, datadiaabertoinicio=datetime.datetime.today() - datetime.timedelta(days=1), datadiaabertofim=datetime.datetime.strptime("2021-04-21", "%Y-%m-%d").date(), datainscricaoatividadesinicio=datetime.datetime.today() - datetime.timedelta(days=1), datainscricaoatividadesfim=datetime.datetime.strptime("2021-04-21", "%Y-%m-%d").date(), datapropostasatividadesincio=datetime.datetime.today() - datetime.timedelta(days=1), dataporpostaatividadesfim=datetime.datetime.strptime("2021-04-21", "%Y-%m-%d").date(), administradorutilizadorid=admin, escalasessoes="11:20")
    
    def test_CriarInscricao(self):
        response = self.c.get('/inscricoes/criar')
        self.assertContains(response, """
        <h2 class="title has-text-grey is-uppercase has-text-centered" style="font-size: 1rem">
            Tipo de Inscrição
        </h2>
        """, 1, html=True)