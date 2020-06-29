from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from django.urls import reverse
from utilizadores.models import Participante
from utilizadores.tests.test_models import create_Participante_0
from notificacoes.tests.test_models import create_MensagemRecebida_0
from selenium.webdriver.support.wait import WebDriverWait

# Firefox, Edge, Safari, Chrome


class CriarParticipante(StaticLiveServerTestCase):
    """ Testes funcionais do criar participante - Sucesso """

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
        self.participante = create_Participante_0()
        self.participante.set_password('andre123456')
        self.participante.save()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def test_criar_participante_ok(self):
        """ Testes funcionais do criar participante - Sucesso """