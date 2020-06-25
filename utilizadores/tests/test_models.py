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
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )[0]    

def create_Administrador_0():
    return Administrador.objects.get_or_create(
        username="andre0",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )[0]


def create_Administrador_1():
    return Administrador.objects.get_or_create(
        username="andre1",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False",
        gabinete="A20",
    )[0]    


def create_Participante_0():
    return Participante.objects.get_or_create(
        username="andre0",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="True"
    )[0]


def create_Participante_1():
    return Participante.objects.get_or_create(
        username="andre1",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="True"
    )[0]    



def create_Campus_0():
    return Campus.objects.get_or_create(nome='Penha')[0]



def create_UO_0(campus):
    return Unidadeorganica.objects.get_or_create(
        nome = 'Faculdade de Ciencias e Tecnologias',
        sigla = 'FCT',
        campusid = campus
        )[0]



def create_Curso_0():
    return Curso.objects.get_or_create(nome="CC",
    sigla="Ciências da Comunicação",
    campus=create_UO_0(create_Campus_0()),
    )[0]



def create_Departamento_0(uo):
    return Departamento.objects.get_or_create(
        nome = 'Departamento de Engenharia Informatica e Eletronica',
        sigla = 'DEEI',
        unidadeorganicaid = uo
    )[0]




def create_ProfessorUniversitario_0():
    return ProfessorUniversitario.objects.get_or_create(
        username="andre0",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False",
        gabinete="A20",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
        
    )[0]


def create_ProfessorUniversitario_1():
    return ProfessorUniversitario.objects.get_or_create(
        username="andre1",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False",
        gabinete="A20",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]    




def create_Coordenador_0():
    return Coordenador.objects.get_or_create(
        username="andre0",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False",
        gabinete="A20",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]


def create_Coordenador_1():
    return Coordenador.objects.get_or_create(
        username="andre1",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False",
        gabinete="A20",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]        



def create_Colaborador_0():
    return Colaborador.objects.get_or_create(
        username="andre0",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False",
        curso=create_Curso_0(),
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))

    )[0]


def create_Colaborador_1():
    return Colaborador.objects.get_or_create(
        username="andre1",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False",
        curso=create_Curso_0(),
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]        


class TestUtilizadoresModels(TestCase):
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
        self.assertEquals(self.utilizador0.full_name(),"André André")
        self.assertEquals(self.utilizador1.full_name(),"André André")




class TestAdministradoresModels(TestCase):
    ''' Testes para o administrador - funções dos modelos da componente utilizadores '''
    
    def setUp(self):
        call_command('create_groups')
        self.utilizador0 = create_Administrador_0()
        self.utilizador1 = create_Administrador_1()
        self.group = Group.objects.get(name='Administrador') 
        self.group.user_set.add(self.utilizador0)
        self.group.user_set.add(self.utilizador1)

    def test_get_profiles(self):
        ''' Teste que verifica o perfil do administrador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getProfiles(),'Administrador')
        self.assertEquals(user1.getProfiles(),'Administrador')


    def test_get_user(self):
        ''' Teste que verifica o a subclasse do utilizador de um dado utilizador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(self.utilizador0,user1.getUser())
        self.assertEquals(self.utilizador1,user.getUser())


    def test_get_profile(self):
        ''' Teste que verifica o perfil do administrador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getUser(),"Administrador")
        self.assertEquals(self.utilizador1.getUser(),"Administrador")


    def test_email_valido_UO(self):
        ''' Teste que verifica pelo email de um utilizador se é da mesma unidade orgânica que outro '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoUO(create_UO_0(create_Campus_0())),True)
        self.assertEquals(user1.emailValidoUO(create_UO_0(create_Campus_0())),True)   


    def test_email_valido_participante(self):
        ''' Teste que verifica que um utilizador é do tipo administrador pelo email '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoParticipante(),True)
        self.assertEquals(user1.emailValidoParticipante(),True)


    def test_full_name(self):
        ''' Teste que verifica se o nome completo de um administrador é correto '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.full_name(),"André André")
        self.assertEquals(user1.full_name(),"André André")




class TestParticipantesModels(TestCase):
    ''' Testes para o participante - funções dos modelos da componente utilizadores '''
    
    def setUp(self):
        call_command('create_groups')
        self.utilizador0 = create_Participante_0()
        self.utilizador1 = create_Participante_1()
        self.group = Group.objects.get(name='Participante') 
        self.group.user_set.add(self.utilizador0)
        self.group.user_set.add(self.utilizador1)

    def test_get_profiles(self):
        ''' Teste que verifica o perfil do participante '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getProfiles(),'Participante')
        self.assertEquals(user1.getProfiles(),'Participante')


    def test_get_user(self):
        ''' Teste que verifica o a subclasse do utilizador de um dado utilizador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(self.utilizador0,user1.getUser())
        self.assertEquals(self.utilizador1,user.getUser())


    def test_get_profile(self):
        ''' Teste que verifica o perfil do participante '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getUser(),"Administrador")
        self.assertEquals(self.utilizador1.getUser(),"Administrador")


    def test_email_valido_UO(self):
        ''' Teste que verifica pelo email de um utilizador se é da mesma unidade orgânica que outro '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoUO(create_UO_0(create_Campus_0())),False)
        self.assertEquals(user1.emailValidoUO(create_UO_0(create_Campus_0())),False)   


    def test_email_valido_participante(self):
        ''' Teste que verifica que um utilizador é do tipo administrador pelo email '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoParticipante(),False)
        self.assertEquals(user1.emailValidoParticipante(),False)


    def test_full_name(self):
        ''' Teste que verifica se o nome completo de um administrador é correto '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.full_name(),"André André")
        self.assertEquals(user1.full_name(),"André André")        



        
class TestProfessorUniversitariosModels(TestCase):
    ''' Testes para o professor universitário - funções dos modelos da componente utilizadores '''
    
    def setUp(self):
        call_command('create_groups')
        self.utilizador0 = create_ProfessorUniversitario_0()
        self.utilizador1 = create_ProfessorUniversitario_1()
        self.group = Group.objects.get(name='ProfessorUniversitario') 
        self.group.user_set.add(self.utilizador0)
        self.group.user_set.add(self.utilizador1)

    def test_get_profiles(self):
        ''' Teste que verifica o perfil do professor universitário '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getProfiles(),'ProfessorUniversitario')
        self.assertEquals(user1.getProfiles(),'ProfessorUniversitario')


    def test_get_user(self):
        ''' Teste que verifica o a subclasse do utilizador de um dado utilizador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(self.utilizador0,user1.getUser())
        self.assertEquals(self.utilizador1,user.getUser())


    def test_get_profile(self):
        ''' Teste que verifica o perfil do professor universitário '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getUser(),"ProfessorUniversitario")
        self.assertEquals(self.utilizador1.getUser(),"ProfessorUniversitario")


    def test_email_valido_UO(self):
        ''' Teste que verifica pelo email de um utilizador se é da mesma unidade orgânica que outro '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoUO(create_UO_0(create_Campus_0())),True)
        self.assertEquals(user1.emailValidoUO(create_UO_0(create_Campus_0())),True)   


    def test_email_valido_participante(self):
        ''' Teste que verifica que um utilizador é do tipo administrador pelo email '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoParticipante(),False)
        self.assertEquals(user1.emailValidoParticipante(),False)


    def test_full_name(self):
        ''' Teste que verifica se o nome completo de um professor universitário é correto '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.full_name(),"André André")
        self.assertEquals(user1.full_name(),"André André")        


        
class TestCoodenadoresModels(TestCase):
    ''' Testes para o coordenador - funções dos modelos da componente utilizadores '''
    
    def setUp(self):
        call_command('create_groups')
        self.utilizador0 = create_Coodenador_0()
        self.utilizador1 = create_Coodenador_1()
        self.group = Group.objects.get(name='Coodenador') 
        self.group.user_set.add(self.utilizador0)
        self.group.user_set.add(self.utilizador1)

    def test_get_profiles(self):
        ''' Teste que verifica o perfil do coordenador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getProfiles(),'Coodenador')
        self.assertEquals(user1.getProfiles(),'Coodenador')


    def test_get_user(self):
        ''' Teste que verifica o a subclasse do utilizador de um dado utilizador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(self.utilizador0,user1.getUser())
        self.assertEquals(self.utilizador1,user.getUser())


    def test_get_profile(self):
        ''' Teste que verifica o perfil do coordenador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getUser(),"Coodenador")
        self.assertEquals(self.utilizador1.getUser(),"Coodenador")


    def test_email_valido_UO(self):
        ''' Teste que verifica pelo email de um utilizador se é da mesma unidade orgânica que outro '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoUO(create_UO_0(create_Campus_0())),True)
        self.assertEquals(user1.emailValidoUO(create_UO_0(create_Campus_0())),True)   


    def test_email_valido_participante(self):
        ''' Teste que verifica que um utilizador é do tipo administrador pelo email '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoParticipante(),False)
        self.assertEquals(user1.emailValidoParticipante(),False)


    def test_full_name(self):
        ''' Teste que verifica se o nome completo de um coordenador é correto '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.full_name(),"André André")
        self.assertEquals(user1.full_name(),"André André")        




        
class TestColaboradoresModels(TestCase):
    ''' Testes para o colaborador - funções dos modelos da componente utilizadores '''
    
    def setUp(self):
        call_command('create_groups')
        self.utilizador0 = create_Colaborador_0()
        self.utilizador1 = create_Colaborador_1()
        self.group = Group.objects.get(name='Colaborador') 
        self.group.user_set.add(self.utilizador0)
        self.group.user_set.add(self.utilizador1)

    def test_get_profiles(self):
        ''' Teste que verifica o perfil do colaborador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getProfiles(),'Colaborador')
        self.assertEquals(user1.getProfiles(),'Colaborador')


    def test_get_user(self):
        ''' Teste que verifica o a subclasse do utilizador de um dado utilizador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(self.utilizador0,user1.getUser())
        self.assertEquals(self.utilizador1,user.getUser())


    def test_get_profile(self):
        ''' Teste que verifica o perfil do colaborador '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.getUser(),"Colaborador")
        self.assertEquals(self.utilizador1.getUser(),"Colaborador")


    def test_email_valido_UO(self):
        ''' Teste que verifica pelo email de um utilizador se é da mesma unidade orgânica que outro '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoUO(create_UO_0(create_Campus_0())),True)
        self.assertEquals(user1.emailValidoUO(create_UO_0(create_Campus_0())),True)   


    def test_email_valido_participante(self):
        ''' Teste que verifica que um utilizador é do tipo administrador pelo email '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.emailValidoParticipante(),False)
        self.assertEquals(user1.emailValidoParticipante(),False)


    def test_full_name(self):
        ''' Teste que verifica se o nome completo de um colaborador é correto '''
        user0=Utilizadores.objects.get(id=self.utilizador0.id)
        user1=Utilizadores.objects.get(id=self.utilizador1.id)
        self.assertEquals(user0.full_name(),"André André")
        self.assertEquals(user1.full_name(),"André André")        
