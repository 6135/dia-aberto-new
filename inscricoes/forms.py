from . import models
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from configuracao.models import Campus
import json
from django.utils.translation import gettext as _
import re


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


def verificar_vagas(sessoes, nalunos):
    # TODO: Verificar se a inscrição corresponde ao nº de vagas
    pass


class SessoesForm(forms.Form):
    sessoes = forms.CharField()
    sessoes_info = forms.CharField()
    # nalunos = forms.IntegerField(min_value=1)

    def clean(self):
        cleaned_data = super().clean()
        try:
            pattern = re.compile('{(\"\d*\":\d*,)*\"\d*\":\d*}|{}')
            if re.match(pattern, cleaned_data['sessoes']) is None:
                raise Exception()
            sessoes_data: dict = json.loads(cleaned_data['sessoes'])
            # nalunos: int = cleaned_data['nalunos']
        except:
            raise forms.ValidationError(
                _("Something went wrong. Please try submiting a new form."))
        vazio = True
        for sessaoid in sessoes_data:
            if sessoes_data[sessaoid] > 0:
                vazio = False
        if not sessoes_data or vazio:
            raise forms.ValidationError(
                _("At least one session must be chosen."))
        # verificar_vagas(sessoes_data, nalunos)


class SubmissaoForm(forms.Form):
    pass
