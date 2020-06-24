from django.test import TestCase
from utilizadores.models import Participante
from inscricoes.models import Escola, Inscricao


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
