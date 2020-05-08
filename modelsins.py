# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Inscricao(models.Model):
    escola = models.ForeignKey('Escola', models.DO_NOTHING, db_column='escola')
    nalunos = models.IntegerField()
    ano = models.IntegerField()
    turma = models.CharField(max_length=255)
    areacientifica = models.CharField(max_length=255)
    participante = models.ForeignKey('Participante', models.DO_NOTHING, db_column='participante')
    diaaberto = models.ForeignKey('Diaaberto', models.DO_NOTHING, db_column='diaaberto')
    horariochegada = models.TimeField(blank=True, null=True)
    horariopartida = models.TimeField(blank=True, null=True)
    localchegada = models.CharField(db_column='Localchegada', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Inscricao'
