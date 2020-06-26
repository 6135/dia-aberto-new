from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utilizadores.tests.test_models import create_Participante_0
from django.urls import reverse
import os
from configuracao.tests.test_models import create_open_day
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from unittest import skipIf

# class TestCriarInscricaoFirefoxFunc(StaticLiveServerTestCase):

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         if os.name == 'posix':
#             webdriver_path = 'webdrivers_executables/linux/geckodriver'
#         elif os.name == 'nt':
#             webdriver_path = 'webdrivers_executables/windows/geckodriver.exe'
#         options = FirefoxOptions()
#         options.add_argument("--start-maximized")
#         cls.driver = webdriver.Firefox(executable_path=f'{webdriver_path}', options=options)
#         cls.driver.implicitly_wait(10)

#     def setUp(self):
#         self.diaaberto = create_open_day()
#         self.participante = create_Participante_0()
#         self.participante.set_password('andre123456')
#         self.participante.save()

#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         super().tearDownClass()

#     def test_login(self):
#         self.driver.get('%s%s' % (self.live_server_url, reverse('utilizadores:login')))
#         self.driver.find_element(By.CSS_SELECTOR, ".button > span:nth-child(2)").click()
#         self.driver.find_element(By.ID, "id_username").click()
#         self.driver.find_element(By.ID, "id_username").send_keys(self.participante.username)
#         self.driver.find_element(By.ID, "id_password").send_keys("andre123456")
#         self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
#         assert self.driver.find_element(By.CSS_SELECTOR, ".message-body strong").text == f"Bem vindo(a) {self.participante.first_name}"
    
#     def test_criarinscricao_info(self):
#         self.test_login()
#         self.driver.get('%s%s' % (self.live_server_url, reverse('inscricoes:criar-inscricao')))
#         self.driver.find_element(By.CSS_SELECTOR, ".navbar-start > .navbar-item").click()
#         assert self.driver.find_element(By.CSS_SELECTOR, ".title").text == "TIPO DE INSCRIÇÃO"


# class TestCriarInscricaoChromeFunc(StaticLiveServerTestCase):

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         if os.name == 'posix':
#             webdriver_path = 'webdrivers_executables/linux/chromedriver'
#         elif os.name == 'nt':
#             webdriver_path = 'webdrivers_executables/windows/chromedriver.exe'
#         options = ChromeOptions()
#         options.add_argument("--start-maximized")
#         cls.driver = webdriver.Chrome(executable_path=f'{webdriver_path}', options=options)
#         cls.driver.implicitly_wait(10)

#     def setUp(self):
#         self.diaaberto = create_open_day()
#         self.participante = create_Participante_0()
#         self.participante.set_password('andre123456')
#         self.participante.save()

#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         super().tearDownClass()

#     def test_login(self):
#         self.driver.get('%s%s' % (self.live_server_url, reverse('utilizadores:login')))
#         self.driver.find_element(By.CSS_SELECTOR, ".button > span:nth-child(2)").click()
#         self.driver.find_element(By.ID, "id_username").click()
#         self.driver.find_element(By.ID, "id_username").send_keys(self.participante.username)
#         self.driver.find_element(By.ID, "id_password").send_keys("andre123456")
#         self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
#         assert self.driver.find_element(By.CSS_SELECTOR, ".message-body strong").text == f"Bem vindo(a) {self.participante.first_name}"
    
#     def test_criarinscricao_info(self):
#         self.test_login()
#         self.driver.get('%s%s' % (self.live_server_url, reverse('inscricoes:criar-inscricao')))
#         self.driver.find_element(By.CSS_SELECTOR, ".navbar-start > .navbar-item").click()
#         assert self.driver.find_element(By.CSS_SELECTOR, ".title").text == "TIPO DE INSCRIÇÃO"


@SkipIf(os.name == 'posix', "O OperaDriver não funciona para Linux")
class TestCriarInscricaoOperaFunc(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if os.name == 'posix':
            webdriver_path = 'webdrivers_executables/linux/operadriver'
        elif os.name == 'nt':
            webdriver_path = 'webdrivers_executables/windows/operadriver.exe'
        options = OperaOptions()
        options.add_argument("--start-maximized")
        cls.driver = webdriver.Opera(executable_path=f'{webdriver_path}', options=options)
        cls.driver.implicitly_wait(10)

    def setUp(self):
        self.diaaberto = create_open_day()
        self.participante = create_Participante_0()
        self.participante.set_password('andre123456')
        self.participante.save()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self):
        self.driver.get('%s%s' % (self.live_server_url, reverse('utilizadores:login')))
        self.driver.find_element(By.CSS_SELECTOR, ".button > span:nth-child(2)").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(self.participante.username)
        self.driver.find_element(By.ID, "id_password").send_keys("andre123456")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        assert self.driver.find_element(By.CSS_SELECTOR, ".message-body strong").text == f"Bem vindo(a) {self.participante.first_name}"
    
    def test_criarinscricao_info(self):
        self.test_login()
        self.driver.get('%s%s' % (self.live_server_url, reverse('inscricoes:criar-inscricao')))
        self.driver.find_element(By.CSS_SELECTOR, ".navbar-start > .navbar-item").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".title").text == "TIPO DE INSCRIÇÃO"


@SkipIf(os.name == 'posix', "Não existe Edge para Linux")
class TestCriarInscricaoEdgeFunc(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        webdriver_path = 'webdrivers_executables/windows/msedgedriver.exe'
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        cls.driver = webdriver.Edge(executable_path=f'{webdriver_path}', options=options)
        cls.driver.implicitly_wait(10)

    def setUp(self):
        self.diaaberto = create_open_day()
        self.participante = create_Participante_0()
        self.participante.set_password('andre123456')
        self.participante.save()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self):
        self.driver.get('%s%s' % (self.live_server_url, reverse('utilizadores:login')))
        self.driver.find_element(By.CSS_SELECTOR, ".button > span:nth-child(2)").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(self.participante.username)
        self.driver.find_element(By.ID, "id_password").send_keys("andre123456")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        assert self.driver.find_element(By.CSS_SELECTOR, ".message-body strong").text == f"Bem vindo(a) {self.participante.first_name}"
    
    def test_criarinscricao_info(self):
        self.test_login()
        self.driver.get('%s%s' % (self.live_server_url, reverse('inscricoes:criar-inscricao')))
        self.driver.find_element(By.CSS_SELECTOR, ".navbar-start > .navbar-item").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".title").text == "TIPO DE INSCRIÇÃO"

