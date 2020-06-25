# from django.test import TestCase
# from django.test import SimpleTestCase
# from django.urls import resolve,reverse
# from utilizadores import views

# #Create your tests here.


# class TestUrlsConsultarUntilizadores(SimpleTestCase):
    
#     def test_url_is_resolved(self):
#         url = reverse('utilizadores:consultar-utilizadores')
#         self.assertEquals(resolve(url).func.__name__, views.consultar_utilizadores.__name__)
        

# class TestUrls(SimpleTestCase):

#     def test_url_is_resolved(self):
#         url = reverse('utilizadores:escolher-perfil')
#         self.assertEquals(resolve(url).func, views.escolher_perfil)
        
#         url = reverse('utilizadores:criar-utilizador')
#         self.assertEquals(resolve(url).func, views.criar_utilizador)
        
#         url = reverse('utilizadores:concluir-registo', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.concluir_registo)

# class TestUrls(SimpleTestCase):

#     def test_url_is_resolved(self):

#         url = reverse('utilizadores:alterar-password')
#         self.assertEquals(resolve(url).func, views.alterar_password)
        


# class TestUrls(SimpleTestCase):

#     def test_url_is_resolved(self):

#         url = reverse('utilizadores:apagar-conta')
#         self.assertEquals(resolve(url).func.__name__, views.apagar_proprio_utilizador.__name__)
        
#         url = reverse('utilizadores:apagar-utilizador', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.apagar_utilizador)
        



# class TestUrls(SimpleTestCase):

#     def test_url_is_resolved(self):

        
#         url = reverse('utilizadores:validar-utilizador')
#         self.assertEquals(resolve(url).func.__name__, views.validar_utilizador.__name__)
        
#         url = reverse('utilizadores:rejeitar-utilizador')
#         self.assertEquals(resolve(url).func, views.rejeitar_utilizador)


# class TestUrls(SimpleTestCase):

#     def test_url_is_resolved(self):

        
#         url = reverse('utilizadores:mensagem', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.mensagem)
        
#         url = reverse('utilizadores:validar', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.enviar_email_validar)
        
#         url = reverse('utilizadores:rejeitar', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.enviar_email_rejeitar)


# class TestUrls(SimpleTestCase):

#     def test_url_is_resolved(self):
        
#         url = reverse('utilizadores:logout')
#         self.assertEquals(resolve(url).func.__name__, views.logout_action.__name__)
        
#         url = reverse('utilizadores:login')
#         self.assertEquals(resolve(url).func, views.login_action)




# class TestUrls(SimpleTestCase):

#     def test_url_is_resolved(self):

#         url = reverse('utilizadores:alterar-utilizador-admin', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.alterar_utilizador_admin)
        
#         url = reverse('utilizadores:alterar-utilizador')
#         self.assertEquals(resolve(url).func, views.alterar_utilizador)


#         url = reverse('utilizadores:mudar-perfil-escolha-admin', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views..mudar_perfil_escolha_admin)
        
#         url = reverse('utilizadores:mudar-perfil-admin', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.mudar_perfil_admin)

#         url = reverse('utilizadores:mudar-perfil-escolha', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.mudar_perfil_escolha
        
#         url = reverse('utilizadores:mudar-perfil', kwargs={'id':1})
#         self.assertEquals(resolve(url).func, views.mudar_perfil)

