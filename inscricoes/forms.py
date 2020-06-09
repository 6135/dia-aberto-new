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
    return (t1start <= t2start <= t1end) or (t2start <= t1start <= t2end)


def verificar_vagas(sessoes, nalunos):
    """
    Retorna ValidationError caso haja conflitos em relação ao número de inscritos nas sessões.
    """
    inscritos_horarios = []
    for sessao in sessoes:
        nalunos_horario = nalunos
        sessao_obj = Sessao.objects.get(pk=sessao)
        for inscritos_horario in inscritos_horarios:
            if horarios_intersetam(sessao_obj.horarioid.inicio, sessao_obj.horarioid.fim, inscritos_horario['inicio'], inscritos_horario['fim']):
                nalunos_horario -= inscritos_horario['ninscritos']
        if sessoes[sessao] > nalunos_horario:
            raise forms.ValidationError(
                _(f"O número de inscritos na sessão da atividade \"{sessao_obj.atividadeid.nome}\", das {sessao_obj.horarioid.inicio.strftime('%H:%M')} às {sessao_obj.horarioid.fim.strftime('%H:%M')} ({sessoes[sessao]}) excede o nº de alunos disponíveis nesse horário ({nalunos_horario})"))
        inscritos_horarios.append({
            'inicio': sessao_obj.horarioid.inicio,
            'fim': sessao_obj.horarioid.fim,
            'ninscritos': sessoes[sessao],
        })


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
            cleaned_data['sessoes'] = json.loads(cleaned_data['sessoes'])
        except:
            raise forms.ValidationError(
                _("Ocorreu um erro inesperado. Por favor, tente submeter uma nova inscrição."))
        vazio = True
        for sessaoid in cleaned_data['sessoes']:
            if cleaned_data['sessoes'][sessaoid] > 0:
                vazio = False
        if not cleaned_data['sessoes'] or vazio:
            raise forms.ValidationError(
                _("Deve inscrever-se, no mínimo, em uma sessão."))
        verificar_vagas(cleaned_data['sessoes'], cleaned_data['nalunos'])


class SubmissaoForm(forms.Form):
    pass
