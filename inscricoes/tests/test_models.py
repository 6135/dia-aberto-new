from django.test import TestCase
from inscricoes.models import Escola, Inscricao, Inscricaoprato, Responsavel
from inscricoes.tests.test_views import create_open_day, create_campus
from utilizadores.tests.test_models import create_Participante_0
import datetime


def create_Escola_0():
    return Escola.objects.get_or_create(
        nome="Escola Secundária de Loulé",
        local="Loulé",
    )[0]


def create_Escola_1():
    return Escola.objects.get_or_create(
        nome="Escola Básica e Secundária do Cadaval",
        local="Cadaval",
    )[0]


def create_Inscricao_0():
    return Inscricao.objects.get_or_create(
        individual=False,
        nalunos=20,
        escola=create_Escola_0(),
        ano=12,
        turma="A",
        areacientifica="Ciências e Tecnologia",
        participante=create_Participante_0(),
        dia=datetime.date(2020, 8, 21),
        diaaberto=create_open_day(),
        meio_transporte='comboio',
        hora_chegada=datetime.time(10, 30, 00),
        local_chegada="Estação de Comboios de Faro",
        entrecampi=True,
    )[0]


def create_Inscricao_1():
    return Inscricao.objects.get_or_create(
        individual=True,
        nalunos=12,
        escola=create_Escola_1(),
        participante=create_Participante_0(),
        dia=datetime.date(2020, 8, 24),
        diaaberto=create_open_day(),
        meio_transporte='autocarro',
        hora_chegada=datetime.time(8, 40, 0),
        local_chegada="Terminal Rodoviário de Faro",
        entrecampi=True,
    )[0]


def create_Inscricao_2():
    return Inscricao.objects.get_or_create(
        individual=False,
        nalunos=20,
        escola=create_Escola_0(),
        ano=11,
        turma="C",
        areacientifica="Línguas e Humanidades",
        participante=create_Participante_0(),
        dia=datetime.date(2020, 8, 21),
        diaaberto=create_open_day(),
        entrecampi=False,
    )[0]


def create_Responsavel_0():
    return Responsavel.objects.get_or_create(
        inscricao = create_Inscricao_0(),
        nome = "Miguel Afonso",
        email = "miguelafonso@mail.mail",
        tel = "+351931231231",
    )[0]


def create_Inscricaoprato_0():
    return Inscricaoprato.objects.get_or_create(
        inscricao = create_Inscricao_0(),
        campus = create_campus(),
        npratosalunos = 300,
        npratosdocentes = 200,
    )[0]


class TestInscricoesModels(TestCase):
    """ Teste suite dos modelos da app "inscricoes" """

    def test_Escola_model(self):
        """ Testes do modelo "Escola" """
        escolas = [create_Escola_0(), create_Escola_1(), ]
        self.assertEquals(str(escolas[0]), "Escola Secundária de Loulé")

    def test_Inscricao_model(self):
        """ Testes do modelo "Inscricao" """
        inscricoes = [create_Inscricao_0(), create_Inscricao_1(),
                      create_Inscricao_2(), ]

    def test_Responsavel_model(self):
        """ Testes do modelo "Responsavel" """
        responsaveis = [create_Responsavel_0()]

    def test_Inscricaoprato_model(self):
        """ Testes do modelo "Inscricaoprato" """
        inscricoesprato = [create_Inscricaoprato_0()]