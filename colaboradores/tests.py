from django.test import TestCase
from django.contrib.auth.models import Group, User
from .models import *
from utilizadores.models import *
from configuracao.models import *
from coordenadores.models import *
from datetime import datetime, timedelta

# class ColaboradoresTestTarefasColaborador(TestCase):
#     ''' Testes unitarios para a componente colaboradores - Testes toda a componente colaborador '''
#     def setUp(self):
#         self.campus = Campus(nome="Penha")
#         self.campus.save()
#         self.u_organica = Unidadeorganica(nome="ESEC", sigla="Escola Superior de Educação e Comunicação",self.campus.id)
#         self.u_organica.save()
#         self.departamento = Departamento(nome="Ciências Sociais e da Educação",sigla="Ciências Sociais e da Educação",self.u_organica.id)
#         self.departamento.save()
#         self.curso = Curso(nome="CC" ,sigla"Ciências da Comunicação",self.u_organica.id)
#         self.curso.save()
#         self.user_colaborador1 = Colaborador(username="colaborador1", password="andre123456", email="teste_colaboradores1@teste_colaboradores.pt",contacto="+351967321393",valido="True",self.curso.id,self.u_organica.id,self.departamento.id)
#         self.user_coordenador1 = Coordenador(username="coordenador1", password="andre123456", email="teste_colaboradores2@teste_colaboradores.pt",contacto="+351967321393",valido="True",gabinete="A20",self.u_organica.id,self.departamento.id)
#         self.user_colaborador1.save()
#         self.user_coordenador1.save()
#         self.tarefa1 = Tarefa(nome="Test1",estado="naoConcluida",tipo="tarefaAcompanhar",create_at=,dia=,colaborador=self.user_colaborador1.id,coordenador=self.user_cordenador1.id)
#         # self.tarefa2 = Tarefa(nome="Test1",estado="naoConcluida",tipo="tarefaAuxiliar",create_at=,dia=,colaborador=self.user_colaborador1.id,coordenador=self.user_cordenador1.id)
#         # self.tarefa3 = Tarefa(nome="Test1",estado="naoConcluida",tipo="tarefaOutra",create_at=,dia=,colaborador=self.user_colaborador1.id,coordenador=self.user_cordenador1.id)
#         # self.tarefa_acompanhar = TarefaAcompanhar(tarefa=self.tarefa1,origem="Cantina",destino=)
#         # self.tarefa_auxiliar = TarefaAuxiliar()
#         # self.tarefa_outra = TarefaOutra()

#     def teste_iniciar_tarefa(self):
#         info = InformacaoMensagem(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
#                               descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
#         info.save()
#         self.assertEqual("teste", info.descricao)



#     def teste_concluir_tarefa(self):
#         info = InformacaoMensagem(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
#                               descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
#         info.save()
#         self.assertEqual("teste", info.descricao)



#     def teste_cancelar_tarefa(self):
#         info = InformacaoMensagem(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
#                               descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
#         info.save()
#         self.assertEqual("teste", info.descricao)      


    
#     def apagar_tarefa_atribuida(self):
#         info = InformacaoMensagem(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
#                               descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
#         info.save()
#         self.assertEqual("teste", info.descricao)         



#     def apagar_tarefa_atribuida_acompanhar(self):
#         info = InformacaoMensagem(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
#                               descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
#         info.save()
#         self.assertEqual("teste", info.descricao)        


    
#     def apagar_tarefa_atribuida_auxiliar(self):
#         info = InformacaoMensagem(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
#                               descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
#         info.save()
#         self.assertEqual("teste", info.descricao)        



        
#     def apagar_tarefa_atribuida_outra(self):
#         info = InformacaoMensagem(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
#                               descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
#         info.save()
#         self.assertEqual("teste", info.descricao)            