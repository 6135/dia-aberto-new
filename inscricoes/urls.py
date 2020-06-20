from django.urls import path, re_path
from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'inscricoes'

urlpatterns = [
    path('api/atividades', views.AtividadesAPIView.as_view(), name="api-atividades"),
    path('criar', views.InscricaoWizard.as_view(),
         name='criar-inscricao'),
    path('<int:pk>/pdf', views.InscricaoPDF,
         name='inscricao-pdf'),
    path('minhasinscricoes', views.MinhasInscricoes.as_view(),
         name='minhas-inscricoes'),
    path('<int:pk>', views.ConsultarInscricao.as_view(),
         name='consultar-inscricao'),
    path('<int:pk>/<int:step>', views.ConsultarInscricao.as_view(),
         name='consultar-inscricao'),
    path('alterar/<int:pk>', views.ConsultarInscricao.as_view(), {'alterar': True},
         'alterar-inscricao'),
    path('alterar/<int:pk>/<int:step>', views.ConsultarInscricao.as_view(), {'alterar': True},
         'alterar-inscricao'),
    path('apagar/<int:pk>', views.ApagarInscricao,
         name='apagar-inscricao'),
    # url('$', ConsultarInscricaoEscola.detail, name='escola'),
    # url('escola', ConsultarInscricaoResponsaveis.escola, name='escola'),
    # url('consultar-inscricao-transporte',  ConsultarInscricaoResponsaveis.transporte, name="transporte"),
    # url('consultar-inscricao-almoço',  ConsultarInscricaoResponsaveis.almoço, name="almoço"),
    # url('consultar-inscricao-sessao',  ConsultarInscricaoResponsaveis.sessoes, name="sessao"),
    path("tabela", views.ConsultarInscricoes.as_view(),
         name="consultar-inscricoes"),
    # url('<int:pk>', ConsultarInscricaoEscola.as_view(), name='consultar-inscricao-escola'),
    # path('consultarinscricoes', ConsultarInscricoes, name='consultar-inscricoes'),

    #path('<int:pk>', ConsultarInscricao.as_view(), name='consultar-inscricao'),
    #path('consultarinscricoes', ConsultarInscricoes, name='consultar-inscricoes')
]
