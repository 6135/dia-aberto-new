from django.urls import path, re_path
from django.conf.urls import url
from .views import ConsultarInscricoesListView, AlterarInscricao, ConsultarInscricaoResponsaveis, ConsultarInscricaoEscola
from django.urls import path
from django.views.generic import RedirectView
from inscricoes.views import ConsultarInscricao
from .views import AlterarInscricao, ConsultarInscricao, ConsultarInscricoes
from . import views

app_name = 'inscricoes'

urlpatterns = [
    path('api/atividades', views.AtividadesAPIView.as_view(), name="api-atividades"),
    path('api/escolas', views.EscolasAPIView.as_view(), name="api-escolas"),
    path('inscricaowizard', views.InscricaoWizard.as_view(),
         name='criar-inscricao'),
    path('alterar/<int:pk>', views.AlterarInscricaoWizard.as_view(),
         name='alterar-inscricao-wizard'),
    path('alterarinscricao', AlterarInscricao, name='alterar-inscricao'),
    path('<int:pk>', ConsultarInscricaoResponsaveis.as_view(),
         name='consultar-inscricao'),
    # url('$', ConsultarInscricaoEscola.detail, name='escola'),
    # url('escola', ConsultarInscricaoResponsaveis.escola, name='escola'),
    # url('consultar-inscricao-transporte',  ConsultarInscricaoResponsaveis.transporte, name="transporte"),
    # url('consultar-inscricao-almoço',  ConsultarInscricaoResponsaveis.almoço, name="almoço"),
    # url('consultar-inscricao-sessao',  ConsultarInscricaoResponsaveis.sessoes, name="sessao"),
    path("tabela/", ConsultarInscricoesListView.as_view()),
    # url('<int:pk>', ConsultarInscricaoEscola.as_view(), name='consultar-inscricao-escola'),
    # path('consultarinscricoes', ConsultarInscricoes, name='consultar-inscricoes'),

    path('<int:pk>', ConsultarInscricao.as_view(), name='consultar-inscricao'),
    path('consultarinscricoes', ConsultarInscricoes, name='consultar-inscricoes')
]
