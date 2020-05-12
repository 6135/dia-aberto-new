
from django.db import models
from utilizadores.models import Colaborador


class Colaboradorhorario(models.Model):
    # Field name made lowercase.
    colaboradorutilizadorid = models.OneToOneField(
        Colaborador, models.CASCADE, db_column='ColaboradorUtilizadorID', primary_key=True)
    # Field name made lowercase.
    horarioid = models.ForeignKey(
        'configuracao.Horario', models.CASCADE, db_column='HorarioID')
    # Field name made lowercase.
    horarioinicio = models.DateField(db_column='HorarioInicio')

    class Meta:
        db_table = 'ColaboradorHorario'
        unique_together = (
            ('colaboradorutilizadorid', 'horarioid', 'horarioinicio'),)
