from django.db import models


class Notificacao(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    criadoem = models.DateTimeField(auto_now_add=True)
    recetor = models.ForeignKey(
            'utilizadores.Utilizador', models.CASCADE)
    class Meta:
        db_table = 'Notificacao'



class NotificacaoAutomatica(Notificacao):
    sigla = models.CharField(max_length=255)
    class Meta:
        db_table = 'NotificacaoAutomatica'

class Mensagem(Notificacao):
    emissor = models.ForeignKey(
            'utilizadores.Utilizador', models.CASCADE)
    class Meta:
        db_table = 'Mensagem'

