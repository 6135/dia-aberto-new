from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import *
from configuracao.models import *
from utilizadores.models import *
from colaboradores.models import *
from coordenadores.models import *
from notificacoes.models import *
from inscricoes.models import *
from configuracao.tests.test_models import create_open_day
from utilizadores.tests.test_models import create_Administrador_0 
import json
import urllib

def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.parse.urlencode(kwargs) # for Python 3, use urllib.parse.urlencode instead

class TestViews(TestCase): 
    
    def setUp(self):
        self.client = Client()
        self.admin = create_Administrador_0()
        self.diaaberto = create_open_day()

    def test_ver_dias(self):
        client  = self.client

        response = client.get(reverse('configuracao:diasAbertos'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:diasAbertos'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=self.admin) #now we test with loggin
        response = client.get(reverse('configuracao:diasAbertos'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'configuracao/listaDiaAberto.html')
        self.assertContains(response,status_code=200,text=str(self.diaaberto.ano)) #vemos se o dia aparece na lista
        self.assertContains(response,status_code=200,text=str(self.diaaberto.descricao))
        self.assertContains(response,status_code=200,text='Criar novo Dia Aberto')
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:') #vemos se o dia aparece na lista

        #agora testamos se o filtro funciona, como so vai haver um ano, podemos verifica se apenas um ano aparece, ou nenhum
        print(url_with_querystring(path=reverse('configuracao:diasAbertos'), ano=datetime.now().year))
        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), ano=datetime.now().year)) #apenas um ano
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=1) #vemos se o dia aparece na lista

        print(url_with_querystring(path=reverse('configuracao:diasAbertos'), diainicio=str(date(1970,1,1))))
        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'),diainicio=str(date(1970,1,1)))) #agora as datas
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=1) #vemos se o dia aparece na lista

        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), diafim=str(date(2040,1,2)) ))
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=1) #vemos se o dia aparece na lista
       
        #no day filter

        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), ano=(datetime.now().year +1) )) #apenas um ano
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=0) #vemos se o dia aparece na lista

        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), diainicio=str(date(2299,5,27)))) #agora as datas
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=0) #vemos se o dia aparece na lista

        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), diafim=str(date(2299,5,27))))
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=0) #vemos se o dia aparece na lista

    def test_novo_dia(self):
        