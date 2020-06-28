from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from django.urls import reverse
from utilizadores.models import Participante
from utilizadores.tests.test_models import create_Participante_0
from inscricoes.tests.test_models import create_Responsavel_0, create_Participante_Rafael
from inscricoes.tests.samples import create_Espaco_0, create_Sessao_0, create_Sessao_1, create_Sessao_2, create_Transporte_0, create_Transportehorario_0, create_Horario_0, create_Horario_1, create_Horario_2
from notificacoes.tests.test_models import create_MensagemRecebida_0
from selenium.webdriver.support.wait import WebDriverWait


def create_Inscricao_1():
    return Inscricao.objects.get_or_create(
        individual=True,
        nalunos=12,
        escola=create_Escola_1(),
        participante=create_Participante_Rafael(),
        dia=datetime.date(2020, 8, 24),
        diaaberto=create_Diaaberto_0(),
        meio_transporte='autocarro',
        hora_chegada=datetime.time(8, 40, 0),
        local_chegada="Terminal Rodoviário de Faro",
        entrecampi=True,
    )[0]


def create_Escola_1():
    return Escola.objects.get_or_create(
        nome="Escola Básica e Secundária do Cadaval",
        local="Cadaval",
    )[0]


def create_ProfessorUniversitario_0():
    return ProfessorUniversitario.objects.get_or_create(
        username="professor",
        first_name="José",
        last_name="Mário",
        password="andre123456",
        email="jose@jose.com",
        contacto="+351910897456",
        valido="True",
        gabinete="1.69",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))

    )[0]

    def create_Participante_Rafael():
    return Participante.objects.get_or_create(
        username="participante",
        first_name="Rafael",
        last_name="Duarte",
        password="andre123456",
        email="rafael@rafael.com",
        contacto="+351910777888",
        valido="True"
    )[0]


def create_Departamento_0(uo):
    return Departamento.objects.get_or_create(
        nome='Departamento de Engenharia Informatica e Eletronica',
        sigla='DEEI',
        unidadeorganicaid=uo
    )[0]


def create_Campus_0():
    return Campus.objects.get_or_create(nome='Gambelas')[0]


def create_UO_0(campus):
    return Unidadeorganica.objects.get_or_create(
        nome='Faculdade de Ciencias e Tecnologias',
        sigla='FCT',
        campusid=campus
    )[0]


def create_Tema_0():
    return Tema.objects.get_or_create(tema="Informatica")[0]


def create_Atividade_0():
    return Atividade.objects.get_or_create(
        nome="Java",
        descricao="Aprendendo Java",
        publicoalvo="Ciencias e Tecnologia",
        nrcolaboradoresnecessario=0,
        tipo='Palestra',
        estado='Aceite',
        professoruniversitarioutilizadorid=create_ProfessorUniversitario_0(),
        duracaoesperada=30,
        participantesmaximo=30,
        diaabertoid=create_Diaaberto_0(),
        espacoid=create_Espaco_0(),
        tema=create_Tema_0(),
    )[0]


class ConsultarInscricaoFirefoxTest(StaticLiveServerTestCase):
    """ Testes funcionais do consultar inscrição no Firefox """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        driver_path = 'webdrivers/geckodriver'
        if os.name == 'nt':
            driver_path += '.exe'
        cls.driver = webdriver.Firefox(executable_path=driver_path)
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        self.participante = create_Participante_Rafael()
        self.participante.set_password('andre123456')
        self.participante.save()
        self.responsavel = create_Responsavel_0()
        self.responsavel.set_password('andre123456')
        self.responsavel.save()
        self.inscricao = create_Inscricao_1()
        self.inscricao.save()
        self.atividade = create_Atividade_0()
        self.atividade.save()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_consultar_inscricoes(self):
