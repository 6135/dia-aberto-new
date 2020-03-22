from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Utilizador(models.Model):
    nome = models.CharField(max_length=128)
    email = models.EmailField()
    telefone = PhoneNumberField()
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    class Meta:
        db_table = 'Utilizador'


class Administrador(Utilizador):
    gabinete = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Administrador'


class Participante(Utilizador):
    class Meta:
        db_table = 'Participante'


class Professoruniversitario(models.Model):
    # Field name made lowercase.
    utilizadorid = models.OneToOneField(
        Utilizador, models.CASCADE, db_column='UtilizadorID', primary_key=True)
    # Field name made lowercase.
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=True, null=True)
    departamento = models.ForeignKey('configuracao.Departamento', models.DO_NOTHING, db_column='departamento')
    class Meta:
        db_table = 'ProfessorUniversitario'
