from django.db import models

from notifications.base.models import AbstractNotification



class Notificacao(AbstractNotification):
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    class Meta(AbstractNotification.Meta):
        abstract = False
        db_table = 'Notificacao'



class MensagemRecebida(models.Model):
    mensagem = models.ForeignKey(
        Notificacao, models.CASCADE)
        
    class Meta:
        db_table = 'MensagemRecebida'



class MensagemEnviada(models.Model):
    mensagem = models.ForeignKey(
        Notificacao, models.CASCADE)

    class Meta:
        db_table = 'MensagemEnviada'

