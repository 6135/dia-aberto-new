from atividades.models import Atividade, Sessao
from configuracao.models import Horario
from rest_framework import serializers


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'


class SessaoSerializer(serializers.ModelSerializer):
    horario = HorarioSerializer(source='horarioid', read_only=True)

    class Meta:
        model = Sessao
        fields = '__all__'


class AtividadeSerializer(serializers.ModelSerializer):
    sessao_set = SessaoSerializer(many=True, read_only=True)
    campus = serializers.CharField(source='get_campus_str')

    class Meta:
        model = Atividade
        fields = '__all__'
