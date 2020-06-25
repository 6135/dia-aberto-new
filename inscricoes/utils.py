from django.contrib.staticfiles import finders
import os
from dia_aberto import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404
from inscricoes.models import Escola, Inscricao, Inscricaosessao
from django.core.mail import EmailMessage
from utilizadores.views import user_check
from utilizadores.models import Administrador, Coordenador, Participante
from django.db import transaction
from atividades.models import Atividade, Sessao
from django.db.models import F
from inscricoes.forms import AlmocoForm, InscricaoForm, ResponsavelForm, SessoesForm, TransporteForm
import json
from configuracao.models import Campus, Departamento, Diaaberto, Menu, Prato, Unidadeorganica
from django.utils.datetime_safe import datetime


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def render_pdf(template_path, context={}, filename="file.pdf", send=False):
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponseBadRequest()
    return response


def enviar_mail_confirmacao_inscricao(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    ano = inscricao.diaaberto.ano
    context = {
        'request': request,
        'inscricao': inscricao,
        'ano': ano,
    }
    subject = f'Confirmação da Inscrição no Dia Aberto de {ano} da Universidade do Algarve.'
    message = f'Exmo(a). {inscricao.responsavel_set.first().nome},\n\n'
    message += 'A sua inscrição no Dia Aberto da Universidade do Algarve foi efectuada com sucesso!\n'
    message += 'Segue em anexo um ficheiro PDF com toda a informação relativa à sua inscricão.\n\n'
    message += 'Cumprimentos, Dia Aberto UAlg.'
    source = settings.EMAIL_HOST_USER
    recipient_list = [inscricao.responsavel_set.first().email, ]
    pdf = render_pdf("inscricoes/pdf.html", context,
                     f"dia_aberto_ualg_{ano}.pdf", True).content
    email = EmailMessage(subject, message, source, recipient_list, attachments=[
                         (f"dia_aberto_ualg_{ano}.pdf", pdf, 'application/pdf')])
    email.send(fail_silently=True)


def coordenador_e_inscricao_nao_do_departamento(request, inscricao):
    user_check_var = user_check(request=request, user_profile=[Coordenador])
    if user_check_var.get('exists'):
        coordenador = Coordenador.objects.get(user_ptr=request.user)
        if coordenador.departamento not in inscricao.get_departamentos():
            return user_check_var.get('render')
    return False


def participante_e_inscricao_doutro(request, inscricao):
    user_check_var = user_check(request=request, user_profile=[Participante])
    if user_check_var.get('exists'):
        participante = Participante.objects.get(user_ptr=request.user)
        if inscricao.participante != participante:
            return user_check_var.get('render')
    return False


def nao_tem_permissoes(request, inscricao):
    user_check_var = user_check(request=request, user_profile=[
                                Coordenador, Participante, Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    if coordenador_e_inscricao_nao_do_departamento(request, inscricao):
        return user_check_var.get('render')
    if participante_e_inscricao_doutro(request, inscricao):
        return user_check_var.get('render')
    return False


def add_vagas_sessao(sessaoid, vagas):
    with transaction.atomic():
        sessao = Sessao.objects.select_for_update().get(pk=sessaoid)
        sessao.vagas = F('vagas') + vagas
        sessao.save()


def init_form(step, inscricao, POST=None):
    form = None
    if step == 'responsaveis':
        responsavel = inscricao.responsavel_set.first()
        form = ResponsavelForm(POST, instance=responsavel)
    elif step == 'escola':
        form = InscricaoForm(POST,
                             instance=inscricao,
                             initial={
                                 'nome_escola': inscricao.escola.nome,
                                 'local': inscricao.escola.local,
                                 'dia': inscricao.dia.strftime("%d/%m/%Y"),
                             })
    elif step == 'transporte':
        initial = {
            'meio': inscricao.meio_transporte,
            'entrecampi': inscricao.entrecampi,
        }
        if initial['meio'] != 'outro':
            initial.update({
                'hora_chegada': inscricao.hora_chegada.strftime("%H:%M"),
                'local_chegada': inscricao.local_chegada,
            })
        form = TransporteForm(POST,
                              initial=initial)
    elif step == 'almoco':
        form = AlmocoForm(POST,
                          instance=inscricao.inscricaoprato_set.first(),
                          initial={
                              'nalunos': inscricao.nalunos,
                              'nresponsaveis': 1,
                              'individual': inscricao.individual,
                          })
    elif step == 'sessoes':
        inscricoes_sessao = inscricao.inscricaosessao_set.all()
        sessoes = {}
        sessoes_info = []
        for inscricao_sessao in inscricoes_sessao:
            sessao = inscricao_sessao.sessao
            sessoes[sessao.id] = inscricao_sessao.nparticipantes
            sessoes_info.append({
                'atividade': {'nome': sessao.atividadeid.nome, 'sala': sessao.atividadeid.get_sala_str()},
                'sessao': {
                    'id': sessao.id,
                    'vagas': sessao.vagas + inscricao_sessao.nparticipantes,
                    'horario': {
                        'inicio': sessao.horarioid.inicio.strftime("%H:%M:%S"),
                        'fim': sessao.horarioid.fim.strftime("%H:%M:%S"),
                    },
                },
            })
        sessoes = json.dumps(sessoes)
        sessoes_info = json.dumps(sessoes_info)
        form = SessoesForm(POST,
                           initial={
                               'sessoes': sessoes,
                               'sessoes_info': sessoes_info,
                               'nalunos': inscricao.nalunos,
                           })
    return form


def update_context(context, step, wizard=None, inscricao=None):
    if step == 'escola':
        prox_diaaberto = Diaaberto.current()
        context.update({
            'escolas': json.dumps(list(set(map(lambda x: x.nome, Escola.objects.all())))),
            'inicio': prox_diaaberto.datadiaabertoinicio.strftime("%d/%m/%Y"),
            'fim': prox_diaaberto.datadiaabertofim.strftime("%d/%m/%Y"),
        })
    elif step == 'almoco':
        diaaberto = Diaaberto.current()
        campi = Campus.objects.all()
        pratos_info = {}
        for tipoid, tipo in Prato.tipos:
            pratos_info[tipo] = {}
            for campus in campi:
                pratos_info[tipo][campus] = []
                menu_filter = Menu.objects.filter(
                    diaaberto=diaaberto, campus=campus)
                if menu_filter.exists():
                    menu = menu_filter.first()
                    for prato in menu.prato_set.filter(tipo=tipoid):
                        pratos_info[tipo][campus].append(prato.__str__())
        campi_str = list(map(lambda x: x.nome, Campus.objects.all()))
        context.update({
            'precoalunos': '%.2f' % diaaberto.precoalunos,
            'precoprofessores': '%.2f' % diaaberto.precoprofessores,
            'campi': campi_str,
            'pratos_info': pratos_info,
            'nalunos': wizard.get_cleaned_data_for_step('escola')['nalunos'] if wizard else inscricao.nalunos,
            'nresponsaveis': 1,
        })
    elif step == 'sessoes':
        print()
        context.update({
            'campus': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Campus.objects.all()))),
            'unidades_organicas': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Unidadeorganica.objects.all()))),
            'departamentos': json.dumps(list(map(lambda x: {'id': x.id, 'nome': x.nome}, Departamento.objects.all()))),
            'tipos': json.dumps(list(map(lambda x: x[0], Atividade.tipos))),
            'publicos_alvo': json.dumps(list(map(lambda x: x[0], Atividade.publicosalvo))),
            'nalunos': wizard.get_cleaned_data_for_step('escola')['nalunos'] if wizard else inscricao.nalunos,
            'dia': wizard.get_cleaned_data_for_step('escola')['dia'].strftime("%d/%m/%Y") if wizard else inscricao.dia.strftime("%d/%m/%Y"),
        })
    elif step == 'submissao':
        context.clear()
        context.update({
            'inscricao': inscricao,
        })


def update_post(step, POST, wizard=None, inscricao=None):
    mutable = POST._mutable
    POST._mutable = True
    prefix = f"{POST.get('inscricao_wizard-current_step', step)}-" if wizard else ''
    if step == 'escola' or wizard and POST.get('inscricao_wizard-current_step', '') == 'escola':
        try:
            dia = datetime.strptime(POST[f'{prefix}dia'], "%d/%m/%Y")
            diaaberto = Diaaberto.objects.filter(
                datadiaabertoinicio__lte=dia.replace(hour=23), datadiaabertofim__gte=dia.replace(hour=0)).first()
            if diaaberto:
                POST[f'{prefix}diaaberto'] = diaaberto.id
        except:
            pass
        POST[f'{prefix}individual'] = wizard.get_cleaned_data_for_step('info')[
            'individual'] if wizard else inscricao.individual
    elif step == 'almoco' or wizard and POST.get('inscricao_wizard-current_step', '') == 'almoco':
        POST[f'{prefix}nalunos'] = wizard.get_cleaned_data_for_step('escola')[
            'nalunos'] if wizard else inscricao.nalunos
        POST[f'{prefix}nresponsaveis'] = 1
        POST[f'{prefix}individual'] = wizard.get_cleaned_data_for_step('info')[
            'individual'] if wizard else inscricao.individual
    elif step == 'sessoes' or wizard and POST.get('inscricao_wizard-current_step', '') == 'sessoes':
        POST[f'{prefix}nalunos'] = wizard.get_cleaned_data_for_step('escola')[
            'nalunos'] if wizard else inscricao.nalunos
        POST[f'{prefix}dia'] = wizard.get_cleaned_data_for_step('escola')[
            'dia'] if wizard else inscricao.dia
    POST._mutable = mutable


def save_form(step, form, inscricao):
    if step == 'almoco':
        almoco = form.save(commit=False)
        if almoco is not None:
            almoco.inscricao = inscricao
            almoco.save()
        else:
            inscricaoalmoco = inscricao.inscricaoalmoco_set.first()
            if inscricaoalmoco:
                inscricaoalmoco.delete()
    if step == 'transporte':
        inscricao.meio_transporte = form.cleaned_data['meio']
        outro = form.cleaned_data['meio'] == 'outro'
        inscricao.hora_chegada = form.cleaned_data['hora_chegada'] if not outro else None
        inscricao.local_chegada = form.cleaned_data['local_chegada'] if not outro else None
        inscricao.entrecampi = form.cleaned_data['entrecampi']
        inscricao.save()
    elif step == 'sessoes':
        for inscricao_sessao in inscricao.inscricaosessao_set.all():
            inscricao_sessao.delete()
        sessoes = form.cleaned_data['sessoes']
        for sessaoid in sessoes:
            if sessoes[sessaoid] > 0:
                inscricao_sessao = Inscricaosessao(sessao=Sessao.objects.get(
                    pk=sessaoid), nparticipantes=sessoes[sessaoid], inscricao=inscricao)
                add_vagas_sessao(sessaoid, -sessoes[sessaoid])
                inscricao_sessao.save()
    else:
        form.save()
