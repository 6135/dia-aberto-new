from . import models
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from configuracao.models import Campus
import json
from django.utils.translation import gettext as _
import re
from atividades.models import Sessao


class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = models.Responsavel
        exclude = ('inscricao',)


class InscricaoForm(forms.ModelForm):
    nome_escola = forms.CharField(max_length=200)
    local = forms.CharField(max_length=128)

    class Meta:
        model = models.Inscricao
        exclude = ('escola', "ninscricao", 'participante')

    def save(self, commit=True):
        self.instance.escola = models.Escola.objects.get_or_create(
            nome=self.cleaned_data['nome_escola'], local=self.cleaned_data['local'])[0]
        return super(InscricaoForm, self).save(commit=commit)


class TransporteForm(forms.Form):
    pass


class AlmocoForm(forms.ModelForm):

    class CampusField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.nome

    campus = CampusField(queryset=Campus.objects.all())

    class Meta:
        model = models.Inscricaoprato
        exclude = ('inscricao',)


def horarios_intersetam(t1start, t1end, t2start, t2end):
    return (t1start <= t2start < t1end) or (t2start <= t1start < t2end)


def verificar_vagas(sessoes, nalunos):
    """
    Retorna ValidationError caso haja conflitos em relação ao número de inscritos nas sessões.
    """
    inscritos_horarios = []
    for sessao in sessoes:
        try:
            horario = Sessao.objects.get(pk=sessao).horarioid
        except:
            raise forms.ValidationError(
                _("Ocorreu um erro inesperado. Por favor, tente submeter uma nova inscrição."))
        inscritos_horarios.append({
            'sessao': sessao,
            'inicio': horario.inicio,
            'fim': horario.fim,
            'ninscritos': sessoes[sessao],
        })
    for sessao in sessoes:
        nalunos_horario = nalunos
        sessao_obj = Sessao.objects.get(pk=sessao)
        if sessoes[sessao] > sessao_obj.vagas:
            raise forms.ValidationError(
                _(f"O número de inscritos na sessão da atividade \"{sessao_obj.atividadeid.nome}\", das {sessao_obj.horarioid.inicio.strftime('%H:%M')} às {sessao_obj.horarioid.fim.strftime('%H:%M')} ({sessoes[sessao]} inscritos) excede o nº de vagas para essa sessão ({sessao_obj.vagas} vagas). Este erro pode ter ocorrido porque foi submetida entretanto uma outra inscrição que ocupou as vagas pretendidas. Por favor, atualize as suas inscrições nas sessões."))
        if sessoes[sessao] > nalunos:
            raise forms.ValidationError(
                _(f"O número de inscritos na sessão da atividade \"{sessao_obj.atividadeid.nome}\", das {sessao_obj.horarioid.inicio.strftime('%H:%M')} às {sessao_obj.horarioid.fim.strftime('%H:%M')} ({sessoes[sessao]} inscritos) excede o nº de alunos disponíveis nesse horário ({nalunos} alunos)."))
        sessoes_simultaneas = []
        for inscritos_horario in inscritos_horarios:
            if inscritos_horario['sessao'] is not sessao and horarios_intersetam(sessao_obj.horarioid.inicio, sessao_obj.horarioid.fim, inscritos_horario['inicio'], inscritos_horario['fim']):
                nalunos_horario -= inscritos_horario['ninscritos']
                sessoes_simultaneas.append(inscritos_horario)
        if sessoes[sessao] > nalunos_horario:
            quote = '"'
            raise forms.ValidationError(
                _(f"O número de inscritos na sessão da atividade \"{sessao_obj.atividadeid.nome}\", das {sessao_obj.horarioid.inicio.strftime('%H:%M')} às {sessao_obj.horarioid.fim.strftime('%H:%M')} ({sessoes[sessao]} inscritos) excede o nº de alunos disponíveis nesse horário ({nalunos_horario} alunos). Sessões simultâneas: {', '.join([quote + Sessao.objects.get(pk=sessao_simultanea['sessao']).atividadeid.nome + quote + ' das ' + sessao_simultanea['inicio'].strftime('%H:%M') + ' às ' + sessao_simultanea['fim'].strftime('%H:%M') + ' (' + str(sessao_simultanea['ninscritos']) + ' inscritos)' for sessao_simultanea in sessoes_simultaneas])}."))


class SessoesForm(forms.Form):
    sessoes = forms.CharField()
    sessoes_info = forms.CharField()
    nalunos = forms.IntegerField(min_value=1)

    def clean(self):
        cleaned_data = super().clean()
        try:
            pattern = re.compile('{(\"\d*\":\d*,)*\"\d*\":\d*}|{}')
            if re.match(pattern, cleaned_data['sessoes']) is None:
                raise Exception()
            _sessoes = json.loads(cleaned_data['sessoes'])
            cleaned_data['sessoes'] = {sessao: _sessoes[sessao]
                                       for sessao in _sessoes if _sessoes[sessao] > 0}
        except:
            raise forms.ValidationError(
                _("Ocorreu um erro inesperado. Por favor, tente submeter uma nova inscrição."))
        if not cleaned_data['sessoes']:
            raise forms.ValidationError(
                _("Deve inscrever-se, no mínimo, em uma sessão."))
        verificar_vagas(cleaned_data['sessoes'], cleaned_data['nalunos'])
