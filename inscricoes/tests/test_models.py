from django.test import TestCase
from inscricoes.models import Escola, Inscricao, Inscricaoprato, Inscricaosessao, Inscricaotransporte, Responsavel
from utilizadores.tests.test_models import create_Participante_0, create_ProfessorUniversitario_0
from configuracao.tests.test_models import create_campus, create_edificio, create_horario, create_open_day, create_sala, create_transporteH
from atividades.tests.test_models import create_atividade, create_sessao, create_tema
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


def create_Escola_2():
    return Escola.objects.get_or_create(
        nome="Universidade do Algarve",
        local="Faro",
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
        inscricao=create_Inscricao_0(),
        nome="Miguel Afonso",
        email="miguelafonso@mail.mail",
        tel="+351931231231",
    )[0]


def create_Responsavel_1():
    return Responsavel.objects.get_or_create(
        inscricao=create_Inscricao_1(),
        nome="Miguel Afonso",
        email="miguelafonso@mail.mail",
        tel="+351931231231",
    )[0]


def create_Inscricaoprato_0():
    return Inscricaoprato.objects.get_or_create(
        inscricao=create_Inscricao_0(),
        campus=create_campus(),
        npratosalunos=20,
        npratosdocentes=2,
    )[0]


def create_Inscricaoprato_1():
    return Inscricaoprato.objects.get_or_create(
        inscricao=create_Inscricao_0(),
        campus=create_campus(),
        npratosalunos=15,
        npratosdocentes=1,
    )[0]


def create_Inscricaosessao_0():
    return Inscricaosessao.objects.get_or_create(
        inscricao=create_Inscricao_0(),
        sessao=create_sessao(create_atividade(create_ProfessorUniversitario_0(), create_open_day(
        ), create_sala(create_edificio(create_campus())), create_tema()), create_horario()),
        nparticipantes=20,
    )[0]


def create_Inscricaosessao_1():
    return Inscricaosessao.objects.get_or_create(
        inscricao=create_Inscricao_0(),
        sessao=create_sessao(create_atividade(create_ProfessorUniversitario_0(), create_open_day(
        ), create_sala(create_edificio(create_campus())), create_tema()), create_horario()),
        nparticipantes=13,
    )[0]


def create_Inscricaosessao_2():
    return Inscricaosessao.objects.get_or_create(
        inscricao=create_Inscricao_1(),
        sessao=create_sessao(create_atividade(create_ProfessorUniversitario_0(), create_open_day(
        ), create_sala(create_edificio(create_campus())), create_tema()), create_horario()),
        nparticipantes=12,
    )[0]


def create_Inscricaotransporte_0():
    return Inscricaotransporte.objects.get_or_create(
        inscricao=create_Inscricao_0(),
        transporte=create_transporteH(create_open_day()),
        npassageiros=20,
    )[0]


def create_Inscricaotransporte_1():
    return Inscricaotransporte.objects.get_or_create(
        inscricao=create_Inscricao_1(),
        transporte=create_transporteH(create_open_day()),
        npassageiros=14,
    )[0]


class TestInscricoesModels(TestCase):
    """ Teste suite dos modelos da app "inscricoes" """

    def test_Escola_model(self):
        """ Testes do modelo "Escola" """
        escolas = [
            create_Escola_0(),
            create_Escola_1(),
            create_Escola_2(),
        ]
        self.assertEquals(
            str(escolas[0]), "Escola Secundária de Loulé - Loulé")
        self.assertEquals(
            str(escolas[1]), "Escola Básica e Secundária do Cadaval - Cadaval")
        self.assertEquals(
            str(escolas[2]), "Universidade do Algarve - Faro")

    def test_Inscricao_model(self):
        """ Testes do modelo "Inscricao" """
        inscricoes = [
            create_Inscricao_0(),
            create_Inscricao_1(),
            create_Inscricao_2(),
        ]

    def test_Responsavel_model(self):
        """ Testes do modelo "Responsavel" """
        responsaveis = [
            create_Responsavel_0(),
            create_Responsavel_1(),
        ]

    def test_Inscricaoprato_model(self):
        """ Testes do modelo "Inscricaoprato" """
        inscricoesprato = [
            create_Inscricaoprato_0(),
            create_Inscricaoprato_1(),
        ]

    def test_Inscricaosessao_model(self):
        """ Testes do modelo "Inscricaosessao" """
        inscricoessessao = [
            create_Inscricaosessao_0(),
            create_Inscricaosessao_1(),
            create_Inscricaosessao_2(),
        ]

    def test_Inscricaotransporte_model(self):
        """ Testes do modelo "Inscricaotransporte" """
        inscricoesprato = [
            create_Inscricaotransporte_0(),
            create_Inscricaotransporte_1(),
        ]
