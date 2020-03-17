# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Notificacao(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    descricao = models.CharField(
        db_column='Descricao', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    criadoem = models.CharField(
        db_column='CriadoEm', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Notificacao'


class Envionotificacao(models.Model):
    # Field name made lowercase.
    notificacaoid = models.OneToOneField(
        Notificacao, models.DO_NOTHING, db_column='NotificacaoID', primary_key=True)
    # Field name made lowercase.
    utilizadorid = models.ForeignKey(
        'utilizadores.Utilizador', models.DO_NOTHING, db_column='UtilizadorID')

    class Meta:
        db_table = 'EnvioNotificacao'
        unique_together = (('notificacaoid', 'utilizadorid'),)
# Unable to inspect table 'RececaoNotificacao'
# The error was: (1146, "Table 'diaAberto.RececaoNotificacao' doesn't exist")
