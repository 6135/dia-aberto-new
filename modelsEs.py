# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Espaco(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    edificio = models.ForeignKey('Edificio', models.DO_NOTHING, db_column='Edificio', blank=True, null=True)  # Field name made lowercase.
    andar = models.CharField(db_column='Andar', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Espaco'


class Edificio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=32)  # Field name made lowercase.
    campus = models.ForeignKey('Campus', models.DO_NOTHING, db_column='Campus')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Edificio'


class Campus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    menuid = models.ForeignKey('Menu', models.DO_NOTHING, db_column='MenuID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Campus'
