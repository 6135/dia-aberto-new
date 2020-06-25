from django.test import TestCase
from utilizadores.models import *

def create_Utilizador_0(self):
    utilizador = Utilizador.objects.create(
        username="andre0", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )


def create_Utilizador_1(self):
    utilizador = Utilizador.objects.create(
        username="andre1", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )    

def create_Administrador_0(self):
    utilizador = Administrador.objects.create(
        username="andre0", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )


def create_Administrador_1(self):
    utilizador = Administrador.objects.create(
        username="andre1", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )    


def create_Participante_0(self):
    utilizador = Participante.objects.create(
        username="andre0", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="True"
    )


def create_Participante_1(self):
    utilizador = Participante.objects.create(
        username="andre1", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="True"
    )    



def create_campus():
    return Campus.objects.create(nome='Penha')



def create_uo(campus):
    return Unidadeorganica.objects.create(
        nome = 'Faculdade de Ciencias e Tecnologias',
        sigla = 'FCT',
        campusid = campus
        )


def create_dep(uo):
    return Departamento.objects.create(
        nome = 'Departamento de Engenharia Informatica e Eletronica',
        sigla = 'DEEI',
        unidadeorganicaid = uo
    )




def create_ProfessorUniversitario_0(self):
    utilizador = ProfessorUniversitario.objects.create(
        username="andre0", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )


def create_ProfessorUniversitario_1(self):
    utilizador = ProfessorUniversitario.objects.create(
        username="andre1", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )    




def create_Coordenador_0(self):
    utilizador = Coordenador.objects.create(
        username="andre0", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )


def create_Coordenador_1(self):
    utilizador = Coordenador.objects.create(
        username="andre1", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )        





def create_Colaborador_0(self):
    utilizador = Colaborador.objects.create(
        username="andre0", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )


def create_Colaborador_1(self):
    utilizador = Colaborador.objects.create(
        username="andre1", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )        


class TestUtilizadoresModels(TestCase):
