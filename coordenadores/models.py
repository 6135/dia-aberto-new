# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    estado = models.CharField(max_length=64)
    coord = models.ForeignKey('utilizadores.Coordenador', models.CASCADE, db_column='CoordenadorUtilizadorID',null=True)  # Field name made lowercase.
    colab = models.ForeignKey('utilizadores.Colaborador', models.CASCADE, db_column='ColaboradorUtilizadorID',null=True,blank=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Tarefa'


    def getDescription(self):
        if self.tipo == "tarefaAcompanhar":
            tmp = TarefaAcompanhar.objects.get(tarefaid=self.id)
        elif self.tipo == "tarefaAuxiliar":   
            tmp = TarefaAuxiliar.objects.get(tarefaid=self.id)
        else:
            tmp = TarefaOutra.objects.get(tarefaid=self.id)
        return tmp.getDescription()

class TarefaAcompanhar(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    origem = models.CharField(max_length=255, db_column='origem', blank=False, null=False)
    destino = models.CharField(max_length=255, db_column='destino', blank=False, null=False)
    dia = models.DateField()
    horario = models.TimeField(blank=False, null=False)
    inscricao = models.ForeignKey('inscricoes.Inscricao', models.CASCADE, db_column='inscricao')
    
    class Meta:
        db_table = 'TarefaAcompanhar'

    def getDescription(self):
        msg = "Acompanhar o grupo "+str(self.inscricao.get_grupo())+" de "+self.origem+" a "+self.destino+" no dia "+self.dia.strftime('%d/%m/%y')+" às "+self.horario.strftime('%H horas e %M minutos')+"."
        return msg
class TarefaAuxiliar(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    sessaoid = models.ForeignKey('atividades.Sessao', models.CASCADE, db_column='sessaoid')

    class Meta:
        db_table = 'TarefaAuxiliar'
    
    def getDescription(self):
        msg = "Auxiliar na atividade "+self.sessaoid.atividadeid.nome+"."
        return msg

class TarefaOutra(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    descricao = models.TextField(db_column='descricao', blank=False, null=False)
    horario = models.TimeField(blank=False, null=False)
    dia = models.DateField()

    class Meta:
        db_table = 'TarefaOutra'

    def getDescription(self):
        msg = self.descricao
        return msg