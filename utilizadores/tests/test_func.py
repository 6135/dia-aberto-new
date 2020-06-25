from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utilizadores.tests.test_models import create_Participante_0
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TestLoginFirefoxFunc(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.participante = create_Participante_0()
        cls.participante.set_password('andre123456')
        cls.participante.save()
        if os.name == 'posix':
            webdriver_path = 'webdrivers_executables/linux/geckodriver'
        elif os.name == 'nt':
            webdriver_path = 'webdrivers_executables/windows/geckodriver.exe'
        cls.driver = webdriver.Firefox(executable_path=f'{webdriver_path}')
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .button").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(self.participante.username)
        self.driver.find_element(By.ID, "id_password").send_keys("andre123456")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        assert self.driver.find_element(By.CSS_SELECTOR, ".message-body strong").text == f"Bem vindo(a) {self.participante.first_name}"


class TestLoginChromeFunc(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.participante = create_Participante_0()
        cls.participante.set_password('andre123456')
        cls.participante.save()
        if os.name == 'posix':
            webdriver_path = 'webdrivers_executables/linux/chromedriver'
        elif os.name == 'nt':
            webdriver_path = 'webdrivers_executables/windows/chromedriver.exe'
        cls.driver = webdriver.Chrome(executable_path=f'{webdriver_path}')
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .button").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(self.participante.username)
        self.driver.find_element(By.ID, "id_password").send_keys("andre123456")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        assert self.driver.find_element(By.CSS_SELECTOR, ".message-body strong").text == f"Bem vindo(a) {self.participante.first_name}"
