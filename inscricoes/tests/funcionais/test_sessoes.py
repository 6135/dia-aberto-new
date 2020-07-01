# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestSessoes():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_sessoes(self):
    self.driver.get("http://127.0.0.1:8000/inscricoes/criar")
    self.driver.set_window_size(1918, 1027)
    self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(2)").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .input").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(3) .input").send_keys("10")
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td > .field .input").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td:nth-child(3) .input").send_keys("10")
    element = self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .input")
    assert element.is_enabled() is True
    element = self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td > .field .input")
    assert element.is_enabled() is True
    self.driver.find_element(By.CSS_SELECTOR, ".is-success > span:nth-child(1)").click()
  