from django.test import TestCase

from django.test import TestCase
from utilizadores.models import *
from configuracao.models import *
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

def create_Utilizador_0():
    return Utilizador.objects.get_or_create(
        username="andre0",
        first_name="André",
        last_name="Barrocas", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )[0]



def create_Utilizador_1():
    return Utilizador.objects.get_or_create(
        username="andre1",
        first_name="André",
        last_name="Barrocas", 
        password="andre123456", 
        email="teste1@teste.pt",
        contacto="+351967321393",
        valido="False"
    )[0]    



def create_Mensagem_0():
    return InformacaoMensagem.objects.get_or_create(
        data=timezone.now() + timedelta(days=5),
        pendente=True, 
        titulo = "teste",
        descricao = "teste", 
        emissor = self.user_emissor , 
        recetor = self.user_recipient, 
        tipo = "register" , 
        lido = False
    )[0]        


def create_Mensagem_1():
    return InformacaoMensagem.objects.get_or_create(
        data=timezone.now() + timedelta(days=5),
        pendente=True, 
        titulo = "teste",
        descricao = "teste", 
        emissor = self.user_emissor , 
        recetor = self.user_recipient, 
        tipo = "register" , 
        lido = False
    )[0]        



def create_NotificacaoNaoImediata_0():
    return InformacaoMensagem.objects.get_or_create(
        data=timezone.now() + timedelta(days=5),
        pendente=True, 
        titulo = "teste",
        descricao = "teste", 
        emissor = self.user_emissor , 
        recetor = self.user_recipient, 
        tipo = "register" , 
        lido = False
    )[0]        


def create_NotificacaoNaoImediata_1():
    return InformacaoMensagem.objects.get_or_create(
        data=timezone.now() + timedelta(days=5),
        pendente=True, 
        titulo = "teste",
        descricao = "teste", 
        emissor = self.user_emissor , 
        recetor = self.user_recipient, 
        tipo = "register" , 
        lido = False
    )[0]        





def create_MensagemRecebida_0():
    return InformacaoMensagem.objects.get_or_create(
        data=timezone.now() + timedelta(days=5),
        pendente=True, 
        titulo = "teste",
        descricao = "teste", 
        emissor = self.user_emissor , 
        recetor = self.user_recipient, 
        tipo = "register" , 
        lido = False
    )[0]        


def create_MensagemRecebida_1():
    return InformacaoMensagem.objects.get_or_create(
        data=timezone.now() + timedelta(days=5),
        pendente=True, 
        titulo = "teste",
        descricao = "teste", 
        emissor = self.user_emissor , 
        recetor = self.user_recipient, 
        tipo = "register" , 
        lido = False
    )[0]       




def create_MensagemEnviada_0():
    return InformacaoMensagem.objects.get_or_create(
        data=timezone.now() + timedelta(days=5),
        pendente=True, 
        titulo = "teste",
        descricao = "teste", 
        emissor = self.user_emissor , 
        recetor = self.user_recipient, 
        tipo = "register" , 
        lido = False
    )[0]        


def create_MensagemEnviada_1():
    return InformacaoMensagem.objects.get_or_create(
        data=timezone.now() + timedelta(days=5),
        pendente=True, 
        titulo = "teste",
        descricao = "teste", 
        emissor = self.user_emissor , 
        recetor = self.user_recipient, 
        tipo = "register" , 
        lido = False
    )[0]        
 


class TestMensagemModels(TestCase):
    ''' Testes para o utilizador - funções dos modelos da componente utilizadores '''
    
    def setUp(self):
        call_command('create_groups')
        self.utilizador0 = create_Utilizador_0()
        self.utilizador1 = create_Utilizador_1()



    def test_get_profiles(self):
        ''' Teste que verifica o perfil do utilizador '''
        self.assertEquals(self.utilizador0.getProfiles(),'')
        self.assertEquals(self.utilizador1.getProfiles(),'')


    def test_get_user(self):
        ''' Teste que verifica o a subclasse do utilizador de um dado utilizador '''
        self.assertEquals(self.utilizador0.getUser(),None)
        self.assertEquals(self.utilizador1.getUser(),None)


    def test_get_profile(self):
        ''' Teste que verifica o perfil do utilizador '''
        self.assertEquals(self.utilizador0.getProfile(),None)
        self.assertEquals(self.utilizador1.getProfile(),None)


    def test_email_valido_UO(self):
        ''' Teste que verifica pelo email de um utilizador se é da mesma unidade orgânica que outro '''
        self.assertEquals(self.utilizador0.emailValidoUO(create_UO_0(create_Campus_0())),False)
        self.assertEquals(self.utilizador1.emailValidoUO(create_UO_0(create_Campus_0())),False)   


    def test_email_valido_participante(self):
        ''' Teste que verifica que um utilizador é do tipo administrador pelo email '''
        self.assertEquals(self.utilizador0.emailValidoParticipante(),False)
        self.assertEquals(self.utilizador1.emailValidoParticipante(),False)


    def test_full_name(self):
        ''' Teste que verifica se o nome completo de um utilizador é correto '''
        self.assertEquals(self.utilizador0.full_name,"André Barrocas")
        self.assertEquals(self.utilizador1.full_name,"André Barrocas")



class TestNotificacaoNaoImediataModels(TestCase):
    ''' Testes para o utilizador - funções dos modelos da componente utilizadores '''




class TestMensagemRecebidaModels(TestCase):
    ''' Testes para o utilizador - funções dos modelos da componente utilizadores '''




class TestMensagemRecebidaEnviada(TestCase):
    ''' Testes para o utilizador - funções dos modelos da componente utilizadores '''
