from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import *
from configuracao.models import *
from utilizadores.models import *
from colaboradores.models import *
from coordenadores.models import *
from notificacoes.models import *
from atividades.models import *
from inscricoes.models import *
from configuracao.tests.test_models import create_open_day
from utilizadores.tests.test_models import create_ProfessorUniversitario_0
import json
import urllib

def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.parse.urlencode(kwargs) # for Python 3, use urllib.parse.urlencode instead

class TestViews(TestCase): 
    
    def setUp(self):
        self.client = Client()
        self.admin = create_ProfessorUniversitario_0
        self.diaaberto = create_open_day()

    def test_ver_dias(self):
        client  = self.client

        response = client.get(reverse('configuracao:diasAbertos'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in
