from django.test import TestCase
from utilizadores.models import *
from configuracao.models import *
from coordenadores.models import *
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from datetime import datetime,date, time

def create_Tarefa_0():
    return Tarefa.objects.get_or_create(
        nome = 'Auxiliar na atividade Java',
        estado = 'naoConcluida',
        coord = coord,
        colab = colab,
        dia = date(2021,4,10),
        horario= time(14,20),
    )

def create_Tarefa_1():
    return Tarefa.objects.get_or_create(
        nome = 'Acompanhar o grupo 3',
        estado = 'Concluida',
        coord = coord,
        colab = colab,
        dia = date(2021,4,11),
        horario= time(16,10),
    )

def create_Tarefa_2():
    return Tarefa.objects.get_or_create(
        nome = 'Fechar a sala 1.63...',
        estado = 'naoAtribuida',
        coord = coord,
        colab = colab,
        dia = date(2021,4,12),
        horario= time(10,45),
    )


def create_Tarefa_Auxiliar():
    return TarefaAuxiliar.objects.get_or_create(
        tarefaid = tarefa,
        sessao = sessao
    )

def create_Tarefa_Acompanhar():
    return TarefaAcompanhar.objects.get_or_create(
        tarefaid = tarefa,
        inscricao = inscricao,
        origem = 'Check in',
        destino = '1.63',
    )

def create_Tarefa_Outra():
    return TarefaOutra.objects.get_or_create(
        tarefaid = tarefa,
        descricao = 'Fechar a sala 1.63 do Edificio 1'
    )





def create_Campus_0():
    return Campus.objects.get_or_create(nome='Penha')[0]



def create_UO_0(campus):
    return Unidadeorganica.objects.get_or_create(
        nome = 'Faculdade de Ciencias e Tecnologias',
        sigla = 'FCT',
        campusid = campus
        )[0]



def create_Curso_0():
    return Curso.objects.get_or_create(
        nome="CC",
        sigla="Ciências da Comunicação",
        unidadeorganicaid=create_UO_0(create_Campus_0()),
        )[0]



def create_Departamento_0(uo):
    return Departamento.objects.get_or_create(
        nome = 'Departamento de Engenharia Informatica e Eletronica',
        sigla = 'DEEI',
        unidadeorganicaid = uo
    )[0]




def create_ProfessorUniversitario_0():
    return ProfessorUniversitario.objects.get_or_create(
        username="andre6",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste6@teste.pt",
        contacto="+351967321393",
        valido="False",
        gabinete="A20",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
        
    )[0]


def create_ProfessorUniversitario_1():
    return ProfessorUniversitario.objects.get_or_create(
        username="andre7",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste7@teste.pt",
        contacto="+351967321393",
        valido="False",
        gabinete="A20",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]    




def create_Coordenador_0():
    return Coordenador.objects.get_or_create(
        username="andre8",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste8@teste.pt",
        contacto="+351967321393",
        valido="False",
        gabinete="A20",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]


def create_Coordenador_1():
    return Coordenador.objects.get_or_create(
        username="andre9",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste9@teste.pt",
        contacto="+351967321393",
        valido="False",
        gabinete="A20",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]        



def create_Colaborador_0():
    return Colaborador.objects.get_or_create(
        username="andre10",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste10@teste.pt",
        contacto="+351967321393",
        valido="False",
        curso=create_Curso_0(),
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]


def create_Colaborador_1():
    return Colaborador.objects.get_or_create(
        username="andre11",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste11@teste.pt",
        contacto="+351967321393",
        valido="False",
        curso=create_Curso_0(),
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]        


class TestColaboradoresModels(TestCase):
    ''' Testes para os colaboradores '''
    
    def setUp(self):
        self.diaaberto = create_open_day()
        self.campus = create_campus()
        self.edificio = create_edificio(self.campus)
        self.espaco = create_sala(self.edificio)
        self.coord = create_Coordenador_0()
        self.colab = create_Colaborador_0()
        self.professor= create_ProfessorUniversitario_0()
        self.tema= create_tema()
        self.atividade = create_atividade(self.professor,self.diaaberto,self.espaco,self.tema)
        self.horario=create_horario(inicio=time(14,0),fim=time(14,30))
        self.sessao= create_sessao(self.atividade,self.horario)
        self.inscricao = create_Inscricao_2()
        self.tarefa_0 = create_Tarefa_0(self.coord,self.colab)
        self.tarefa_1 = create_Tarefa_1(self.coord,self.colab)
        self.tarefa_2 = create_Tarefa_2(self.coord,None)
        self.auxiliar = create_Tarefa_auxiliar(self.tarefa_0,self.sessao)
        self.acompanhar = create_Tarefa_acompanhar(self.tarefa_1,self.inscricao)
        self.outra = create_Tarefa_outra(self.tarefa_2)
    
    
    def teste_iniciar_tarefa(self):
        ''' Teste que verifica se uma tarefa é iniciada corretamente '''
        tarefa0 = self.tarefa_0
        tarefa1 = self.tarefa_1
        tarefa0.estado="Iniciada"
        tarefa1.estado="Iniciada"
        self.assertEqual(self.tarefa_0.estado, "Iniciada")
        self.assertEqual(self.tarefa_1.estado, "Iniciada")



    def teste_concluir_tarefa(self):
        ''' Teste que verifica se uma tarefa é concluída corretamente '''
        tarefa0 = self.tarefa_0
        tarefa1 = self.tarefa_1
        tarefa0.estado="Concluida"
        tarefa1.estado="Concluida"
        self.assertEqual(self.tarefa_0.estado, "Concluida")
        self.assertEqual(self.tarefa_1.estado, "Concluida")



    def teste_cancelar_tarefa(self):
        ''' Teste que verifica se uma tarefa é cancelada corretamente '''
        tarefa0 = self.tarefa_0
        tarefa1 = self.tarefa_1
        tarefa0.estado="Cancelada"
        tarefa1.estado="Cancelada"
        self.assertEqual(self.tarefa_0.estado, "Cancelada")
        self.assertEqual(self.tarefa_1.estado, "Cancelada")


    
    def apagar_tarefa_atribuida(self):
        ''' Teste que verifica se uma tarefa é atribuída corretamente '''
        tarefa = self.tarefa_0
        tarefa1 = self.tarefa_1
        self.assertEquals(tarefa.colab.id,self.colab.id)    
        self.assertEquals(tarefa.colab.id,self.colab.id)



    def apagar_tarefa_nao_atribuida(self):
        ''' Teste que verifica se uma tarefa deixa de estar atribuída corretamente '''
        tarefa = self.tarefa_2
        self.assertEquals(tarefa.colab,None)

    
    def test_auxiliar(self):
        ''' Teste para tarefas auxiliares '''
        tarefa = self.auxiliar
        self.assertEquals(tarefa.tarefaid.id,self.tarefa_0.id) 
        self.assertEquals(tarefa.sessao.id,self.sessao.id) 


    def test_acompanhar(self):
        ''' Teste para tarefas de acompanhar '''
        tarefa = self.acompanhar
        self.assertEquals(tarefa.tarefaid.id,self.tarefa_1.id) 
        self.assertEquals(tarefa.inscricao.id,self.inscricao.id)


    def test_outra(self):
        ''' Teste outras tarefas '''
        tarefa = self.outra
        self.assertEquals(tarefa.tarefaid.id,self.tarefa_2.id) 

