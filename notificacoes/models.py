# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Notificacao(models.Model):
    descricao = models.CharField(max_length=255)
    criadoem = models.CharField(max_length=255)

    class Meta:
        db_table = 'Notificacao'


class Envionotificacao(models.Model):
    notificacao = models.ForeignKey(
        Notificacao, models.CASCADE)
    utilizador = models.ForeignKey(
        'utilizadores.Utilizador', models.CASCADE)

    class Meta:
        db_table = 'EnvioNotificacao'
# Unable to inspect table 'RececaoNotificacao'
# The error was: (1146, "Table 'diaAberto.RececaoNotificacao' doesn't exist")
