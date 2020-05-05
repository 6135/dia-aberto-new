# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Transporte(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    identificador = models.CharField(db_column='Identificador', max_length=32, blank=True, null=True)  # Field name made lowercase.
    dia = models.DateField(db_column='Dia', blank=True, null=True)  # Field name made lowercase.
    diaaberto = models.ForeignKey('Diaaberto', models.DO_NOTHING, db_column='Diaaberto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transporte'
