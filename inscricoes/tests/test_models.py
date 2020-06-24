from django.test import TestCase
from inscricoes.models import Escola, Inscricao
from inscricoes.tests.test_views import create_open_day
from utilizadores.tests.test_models import create_Participante_0

def create_Escola_0():
    return Escola.objects.get_or_create(
        nome = "Escola Secundária de Loulé",
        local = "Loulé",
    )

def create_Escola_1():
    return Escola.objects.get_or_create(
        nome = "Escola Básica e Secundária do Cadaval",
        local = "Cadaval",
    )

def create_Inscricao_0():
    return Inscricao.objects.create(
        individual = False,
        nalunos = 20,
        escola = create_Escola_0(),
        ano = 12,
        turma = "A",
        areacientifica = "Ciências e Tecnologia",
        participante = create_Participante_0(),
    )
    create_open_day()

class TestInscricoesModels(TestCase):
    
    def test_Escola_model(self):
        escola = create_Escola_0()
        self.assertEquals(str(escola), "Escola Secundária de Loulé")

    def test_Inscricao_model(self):
        pass