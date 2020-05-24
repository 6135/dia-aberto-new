from django.db import models

from notifications.base.models import AbstractNotification



class Notificacao(AbstractNotification):
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255) 
    tipo = models.CharField(max_length=255)     
    class Meta(AbstractNotification.Meta):
        abstract = False
        db_table = 'Notificacao'




class EmissorMensagem(models.Model):
    mensagem = models.ForeignKey(
        Notificacao, models.CASCADE)
    emissor = models.ForeignKey(
        'utilizadores.Utilizador', models.CASCADE)

    class Meta:
        db_table = 'EmissorMensagem'



class RecetorMensagem(models.Model):
    mensagem = models.ForeignKey(
        Notificacao, models.CASCADE)
    recetor = models.ForeignKey(
        'utilizadores.Utilizador', models.CASCADE)

    class Meta:
        db_table = 'RecetorMensagem'
