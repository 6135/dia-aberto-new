from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Utilizador(User):
    contacto = PhoneNumberField(max_length=20, blank=False , null=False)
    valido = models.CharField(max_length=255, blank=False, null=False)
    def getProfiles(self):
        type = '' 
        if Administrador.objects.filter(utilizador_ptr_id=self):
            type=self.concat(type=type,string='Administrador')
        if Participante.objects.filter(utilizador_ptr_id=self):
            type=self.concat(type=type,string='Participante')
        if ProfessorUniversitario.objects.filter(utilizador_ptr_id=self):
            type=self.concat(type=type,string='Professor Universitario')
        if Coordenador.objects.filter(utilizador_ptr_id=self):
            type=self.concat(type=type,string='Coordenador')
        if Colaborador.objects.filter(utilizador_ptr_id=self):
            type=self.concat(type=type,string='Colaborador')
        return type

    def concat(self,type,string):  
        if type=='':
            type=string
        else:
            type+=', '+string
        return type

    def firstProfile(self):
        return self.getProfiles().split(' ')[0]
    class Meta:
        db_table = 'Utilizador'


class Administrador(Utilizador):
    gabinete = models.CharField(max_length=255, blank=False, null=False)
    class Meta:
        db_table = 'Administrador'



class Participante(Utilizador):
    class Meta:
        db_table = 'Participante'



class ProfessorUniversitario(Utilizador):
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=False, null=False)

    faculdade = models.ForeignKey(
        'configuracao.Unidadeorganica', models.CASCADE)

    departamento = models.ForeignKey(
        'configuracao.Departamento', models.CASCADE)

    class Meta:
        db_table = 'ProfessorUniversitario'


class Coordenador(Utilizador):
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=False, null=False)

    
    faculdade = models.ForeignKey(
        'configuracao.Unidadeorganica', models.CASCADE, db_column='FaculdadeID')

    departamento = models.ForeignKey(
        'configuracao.Departamento', models.CASCADE, db_column='DepartamentoID')
    class Meta:
        db_table = 'Coordenador'

    def __str__(self):
        return self.first_name

class Colaborador(Utilizador):
    curso = models.ForeignKey(
        'configuracao.Curso', models.CASCADE)
        
    faculdade = models.ForeignKey(
        'configuracao.Unidadeorganica', models.CASCADE)

    departamento = models.ForeignKey(
        'configuracao.Departamento', models.CASCADE)
    class Meta:
        db_table = 'Colaborador'



