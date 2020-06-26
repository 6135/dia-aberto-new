from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import *
from configuracao.models import *
from utilizadores.models import *
from colaboradores.models import *
from coordenadores.models import *
from notificacoes.models import *
from inscricoes.models import *
from configuracao.tests.test_models import create_campus, create_curso, create_dep, create_edificio, create_horario, create_menu, create_open_day, create_prato, create_sala, create_transporteH, create_transporteU, create_uo
from utilizadores.tests.test_models import create_Administrador_0, create_Coordenador_0
from datetime import time
import json

import urllib
import pytz

def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.parse.urlencode(kwargs) # for Python 3, use urllib.parse.urlencode instead

class TestViews(TestCase): 
    
    def setUp(self):
        self.client = Client()
        self.diaaberto = create_open_day()
        self.campus = create_campus()
        self.uo = create_uo(self.campus)
        self.dep = create_dep(self.uo)
        self.curso = create_curso(self.uo)
        self.lunchTime = create_horario(inicio=time(12,0),fim=time(14,0))
        self.menu = create_menu(
            campus=self.campus,
            horario=self.lunchTime,
            diaaberto=self.diaaberto
        )
        self.prato = create_prato(menu=self.menu)
        self.edificio = create_edificio(self.campus)
        self.espaco = create_sala(self.edificio)
        self.transporteH = create_transporteH(self.diaaberto)
        self.transporte = self.transporteH.transporte
        self.transporteU = create_transporteU(self.transporte)
        self.admin = create_Administrador_0()
        

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
        #print(url_with_querystring(path=reverse('configuracao:diasAbertos'), ano=datetime.now().year))
        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), ano=datetime.now().year)) #apenas um ano
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=1) #vemos se o dia aparece na lista

        #print(url_with_querystring(path=reverse('configuracao:diasAbertos'), diainicio=str(date(1970,1,1))))
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
        client = self.client

        response = client.get(reverse('configuracao:novoDia'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:novoDia'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')


        client.force_login(user=self.admin) #now we test with loggin
        response = client.get(reverse('configuracao:novoDia'))

        self.assertNotEquals(response.status_code,200)
        self.assertEquals(response.status_code,302)
        self.assertTemplateNotUsed(response, 'configuracao/diaAbertoForm.html') #it cant be right because current day is still open


        response = client.get(reverse('configuracao:novoDia'),follow=True)#if we follow the redirect...

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'configuracao/listaDiaAberto.html') 
       
    def test_new_day_POST(self):
        client = self.client

        client.force_login(user=self.admin) #now we test with loggin
        Diaaberto.objects.all().delete()
        data = {
            'precoalunos': 2,
            'precoprofessores': 2,
            'enderecopaginaweb': 'web.com',
            'descricao': 'Dia Aberto',
            'emaildiaaberto': 'web@web.com',
            'ano': '1970',
            'datadiaabertoinicio': '1970-01-01 9:30',
            'datadiaabertofim': '2040-01-02 9:30',
            'datainscricaoatividadesinicio': '1970-01-01 09:30',
            'datainscricaoatividadesfim': '2040-01-02 09:30',
            'datapropostasatividadesincio': '1970-01-01 09:30',
            'dataporpostaatividadesfim': '2040-01-02 09:30',
            'escalasessoes': '00:31',
        }
        response = client.post(reverse('configuracao:novoDia'), data=data)
        self.assertEquals(response.status_code,302) #302 means it inserted a redirected
        
        self.assertEquals(len(Diaaberto.objects.filter()),1)  
        self.assertEquals(Diaaberto.objects.filter(ano='1970').first().escalasessoes,time(0,31))

        Diaaberto.objects.all().delete()
        data['ano'] = '1971'
        data['datadiaabertoinicio'] = '2040-01-02 1287:30' #formato errado, deve falhar
        response = client.post(reverse('configuracao:novoDia'), data=data)
        self.assertContains(response, status_code=200 ,text = 'Introduza uma data') #back to same page with error
        self.assertEquals(len(Diaaberto.objects.filter()),0)        

    def test_del_day_permissions(self):
        client = self.client
        response = client.get(reverse('configuracao:eliminarDia', kwargs={'id':self.diaaberto.id}))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:eliminarDia', kwargs={'id':self.diaaberto.id}),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:eliminarDia', kwargs={'id':self.diaaberto.id}))
        self.assertEquals(response.status_code,200) #200 means it printed the error message on return (success is a redirect)

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:eliminarDia', kwargs={'id':self.diaaberto.id}))
        self.assertEquals(response.status_code,302) #redirect means it worked
        self.assertEquals(len(Diaaberto.objects.filter()),0) #must be empty!

    def test_view_menus(self):
        client = self.client

        response = client.get(reverse('configuracao:verMenus'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:verMenus'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:verMenus'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:verMenus'))
        self.assertContains(response,status_code=200,text='Feijoada')
        self.assertContains(response,status_code=200,text='Carne')



       
#<
#QueryDict: {'csrfmiddlewaretoken': ['wnVI0xRKO8X7DGgbZS9g24r16kiAdEj6dIepN9xrt337AV3ioOgBm1FcB5cUKO7I'], 
#'campus': ['1'],
#'diaaberto': ['10']
#'dia': ['2021-05-23']
#'form-TOTAL_FORMS': ['1']
#'form-INITIAL_FORMS': ['1']
#'form-MIN_NUM_FORMS': ['1']
#'form-MAX_NUM_FORMS': ['1000'],
#'form-0-id': ['24'],
#'form-0-prato':['Carne Alentejana'],
#'form-0-tipo': ['Carne'],
#'form-0-nrpratosdisponiveis': ['1']}
#>



