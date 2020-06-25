# from django.urls import resolve,reverse
# from utilizadores import views
# from django.test import Client, SimpleTestCase, TestCase
# from utilizadores.models import *
# from django.utils.datetime_safe import datetime
# import pytz
# from django.urls import reverse



# #Create your tests here.


# class TestUrlsConsultarUntilizadores(SimpleTestCase):
#     """ Teste suite dos urls da app "utilizadores" - Caso de uso consultar utilizadores """

#     @classmethod
#     def setUpTestData(cls):
#         cls.participante = create_Participante_0()
         

#     def setUp(self):
#         self.client.force_login(self.participante)
    
    
#     def test_url_consultar_utilizadores(self):
#         """ Testes do url "consultar-utilizadores" """
#         url = reverse('utilizadores:consultar-utilizadores')
#         self.assertEquals(resolve(url).func.__name__, views.consultar_utilizadores.__name__)
        

# class TestCriarUtilizadoresUrls(SimpleTestCase):
#     """ Teste suite dos urls da app "utilizadores" - Caso de uso criar utilizador """
#     @classmethod
#     def setUpTestData(cls):
#         cls.participante = create_Participante_0()
         

#     def setUp(self):
#         self.client.force_login(self.participante)
    
#     def test_url_escolher_perfil_self):
#         """ Testes do url "escolher-perfil" """
#         url = reverse('utilizadores:escolher-perfil')
#         self.assertEquals(resolve(url).func, views.escolher_perfil)
    
#     def test_url_criar_utilizador_self):    
#         """ Testes do url "criar-utilizador" """
#         url = reverse('utilizadores:criar-utilizador')
#         self.assertEquals(resolve(url).func, views.criar_utilizador)
    
#     def test_url_concluir_registo_self): 
#         """ Testes do url "concluir-registo" """   
#         url = reverse('utilizadores:concluir-registo', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.concluir_registo)


# class TestAlterarPasswordUrls(SimpleTestCase):
#     """ Teste suite dos urls da app "utilizadores" - Caso de uso alterar password """
#     @classmethod
#     def setUpTestData(cls):
#         cls.participante = create_Participante_0()
         

#     def setUp(self):
#         self.client.force_login(self.participante)
    
#     def test_url_alterar_password(self):
#         """ Testes do url "alterar-password" """
#         url = reverse('utilizadores:alterar-password')
#         self.assertEquals(resolve(url).func, views.alterar_password)
        


# class TestApagarUtilizadorUrls(SimpleTestCase):
#     """ Teste suite dos urls da app "utilizadores" - Caso de uso apagar conta e apagar utilizador """
#     @classmethod
#     def setUpTestData(cls):
#         cls.participante = create_Participante_0()
         

#     def setUp(self):
#         self.client.force_login(self.participante)

#     def test_url_apagar_conta(self):
#         """ Testes do url "apagar-conta" """
#         url = reverse('utilizadores:apagar-conta')
#         self.assertEquals(resolve(url).func.__name__, views.apagar_proprio_utilizador.__name__)
    
    
#     def test_url_apagar_utilizador(self):    
#         """ Testes do url "apagar-utilizador" """
#         url = reverse('utilizadores:apagar-utilizador', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.apagar_utilizador)
        



# class TestValidarRejeitarUrls(SimpleTestCase):
#     """ Teste suite dos urls da app "utilizadores" - Validar e rejeitar utilizadores """
#     @classmethod
#     def setUpTestData(cls):
#         cls.participante = create_Participante_0()
         

#     def setUp(self):
#         self.client.force_login(self.participante)

#     def test_url_validar(self):
#         """ Testes do url "validar-utilizador" """
#         url = reverse('utilizadores:validar-utilizador')
#         self.assertEquals(resolve(url).func.__name__, views.validar_utilizador.__name__)
    
#     def test_url_validar(self):    
#         """ Testes do url "rejeitar-utilizador" """
#         url = reverse('utilizadores:rejeitar-utilizador')
#         self.assertEquals(resolve(url).func, views.rejeitar_utilizador)


# class TestMensagensUrls(SimpleTestCase):

#     """ Teste suite dos urls da app "utilizadores" - Mensagens """
#     @classmethod
#     def setUpTestData(cls):
#         cls.participante = create_Participante_0()
         

#     def setUp(self):
#         self.client.force_login(self.participante)

#     def test_url_is_resolved(self):

#         url = reverse('utilizadores:mensagem', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.mensagem)


#     def test_url_is_resolved(self):
#         """ Testes do url "validar" """
#         url = reverse('utilizadores:validar', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.enviar_email_validar)

#     def test_url_is_resolved(self):
#         """ Testes do url "rejeitar" """
#         url = reverse('utilizadores:rejeitar', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.enviar_email_rejeitar)






# class TestAlterarPerfilUrls(SimpleTestCase):
    
#     """ Teste suite dos urls da app "utilizadores" - Caso de uso alterar perfil de utilizadores """
#     @classmethod
#     def setUpTestData(cls):
#         cls.participante = create_Participante_0()
         

#     def setUp(self):
#         self.client.force_login(self.participante)


#     def test_url_is_alterar_utilizador_admin(self):
#         """ Testes do url "rejeitar-utilizador" """
#         url = reverse('utilizadores:alterar-utilizador-admin', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.alterar_utilizador_admin)
    
#     def test_url_is_alterar_utilizador(self):  
#         """ Testes do url "alterar-utilizador" """
#         url = reverse('utilizadores:alterar-utilizador')
#         self.assertEquals(resolve(url).func, views.alterar_utilizador)

#     def test_url_is_alterar_perfil_escolha(self): 
#         """ Testes do url "mudar-perfil-escolha-admin" """
#         url = reverse('utilizadores:mudar-perfil-escolha-admin', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views..mudar_perfil_escolha_admin)

#     def test_url_is_alterar_perfil_admin(self): 
#         """ Testes do url "mudar-perfil-admin" """
#         url = reverse('utilizadores:mudar-perfil-admin', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.mudar_perfil_admin)

#     def test_url_is_alterar_perfil_escolha(self): 
#         """ Testes do url "mudar-perfil-escolha" """
#         url = reverse('utilizadores:mudar-perfil-escolha', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.mudar_perfil_escolha

#     def test_url_is_alterar_perfil(self): 
#         """ Testes do url "mudar-perfil" """
#         url = reverse('utilizadores:mudar-perfil', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.mudar_perfil)





# class TestLoginUrls(SimpleTestCase):
    
#     @classmethod
#     def setUpTestData(cls):
#         cls.participante = create_Participante_0()
         

#     def setUp(self):
#         self.client.force_login(self.participante)


#         # url = reverse('utilizadores:logout')
#         # self.assertEquals(resolve(url).func.__name__, views.logout_action.__name__)
        
#         # url = reverse('utilizadores:login')
#         # self.assertEquals(resolve(url).func, views.login_action)

# ###

#     def test_url_inscricao_pdf(self):
#         """ Testes do url "<int:pk>/pdf" de nome inscricao-pdf """
#         inscricao = create_Inscricao_0()
#         response = self.client.get(
#             reverse('inscricoes:inscricao-pdf')
#         self.assertEqual(response.resolver_match.func, InscricaoPDF)
# ###

#     def test_url_login(self):
#         """ Testes do url "login" """
#         response = self.client.get(reverse('utilizadores:login'))
#         self.assertEqual(response.resolver_match.func.__name__,
#                          Login)

#     def test_url_logout(self):
#         """ Testes do url "logout" de nome inscricao-pdf """
#         response = self.client.get(
#             reverse('utilizadores:logout', kwargs={"pk": inscricao.pk}))
#         self.assertEqual(response.resolver_match.func, InscricaoPDF)
