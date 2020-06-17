# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class Anfiteatro(models.Model):
    espacoid = models.OneToOneField('configuracao.Espaco', models.CASCADE, db_column='EspacoID', primary_key=True)  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Anfiteatro'

   
class Arlivre(models.Model):
    espacoid = models.OneToOneField('configuracao.Espaco', models.CASCADE, db_column='EspacoID', primary_key=True)  # Field name made lowercase.
    espacoedificio = models.CharField(db_column='EspacoEdificio', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ArLivre'

class Tema(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tema = models.CharField(db_column='Tema', max_length=64)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tema'

class Atividade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase.
    publicosalvo = (("Ciencias e Tecnologia", "Ciências e Tecnologia"),("Linguas e Humanidades", "Linguas e Humanidades"),("Economia", "Economia"))
    publicoalvo = models.CharField(db_column='Publicoalvo', max_length=255, choices=publicosalvo, default='')  # Field name made lowercase.
    nrcolaboradoresnecessario = models.IntegerField(db_column='nrColaboradoresNecessario')  # Field name made lowercase.
    tipos = (("Atividade Laboratorial", "Atividade Laboratorial"),("Tertulia", "Tertulia"),("Palestra", "Palestra"))
    tipo = models.CharField(db_column='Tipo', max_length=64, choices=tipos, default='Palestra')  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=64)  # Field name made lowercase.
    coordenadorutilizadorid = models.ForeignKey('utilizadores.Coordenador', models.CASCADE, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    professoruniversitarioutilizadorid = models.ForeignKey('utilizadores.ProfessorUniversitario', models.CASCADE, db_column='ProfessorUniversitarioUtilizadorID')  # Field name made lowercase.
    datasubmissao = models.DateTimeField(db_column='dataSubmissao',auto_now_add=True)  # Field name made lowercase.
    dataalteracao = models.DateTimeField(db_column='dataAlteracao',auto_now=True)  # Field name made lowercase.
    duracaoesperada = models.IntegerField(db_column='duracaoEsperada')  # Field name made lowercase.
    participantesmaximo = models.IntegerField(db_column='participantesMaximo')  # Field name made lowercase.
    diaabertoid = models.ForeignKey('configuracao.Diaaberto', models.CASCADE, db_column='diaAbertoID')  # Field name made lowercase.
    espacoid = models.ForeignKey('configuracao.Espaco', models.CASCADE, db_column='EspacoID')  # Field name made lowercase.
    tema = models.ForeignKey('Tema', models.CASCADE, db_column='Tema', blank=False, null=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Atividade'

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Atividade._meta.fields]

    def get_dias(self):
        sessoes= Sessao.objects.filter(atividadeid=self)
        dias = [sessao.dia for sessao in sessoes]
        return [{'key':str(dia), 'value': dia} for dia in set(dias)]
        
    def get_dias_list(self):
        sessoes= Sessao.objects.filter(atividadeid=self)
        dias = [sessao.dia for sessao in sessoes]
        return [dia for dia in set(dias)]

    def get_campus_str(self):
        return self.espacoid.edificio.campus.__str__()

    #def get_uo(self):
    #    return str(self.professoruniversitarioutilizadorid.faculdade)
    
class Materiais(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    atividadeid = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.
    nomematerial = models.CharField(db_column='nome',max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Materiais'

class Sessao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    horarioid = models.ForeignKey('configuracao.Horario', models.DO_NOTHING, db_column='HorarioID')  # Field name made lowercase.
    ninscritos = models.IntegerField(db_column='NInscritos')  # Field name made lowercase.
    vagas = models.IntegerField(db_column='Vagas')  # Field name made lowercase.
    atividadeid = models.ForeignKey(Atividade, models.DO_NOTHING, db_column='AtividadeID')  # Field name made lowercase.
    dia = models.DateField(db_column='Dia', blank=True, null=True)  # Field name made lowercase.

    def timeRange_(self, seperator = ' até '):
        return self.horarioid.inicio.strftime('%H:%M') + str(seperator) + self.horarioid.fim.strftime('%H:%M')
        
    class Meta:
        db_table = 'Sessao'

    def __str__(self):
        return str(self.id)
    


