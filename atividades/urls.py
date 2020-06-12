from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'atividades'

urlpatterns = [
    url(r'^minhasatividades/$',views.minhasatividades,name="minhasAtividades"),
    url(r'^atividadadesUOrganica/$',views.atividadescoordenador,name="atividadesUOrganica"),
    path('alteraratividade/<int:id>',views.alterarAtividade,name='alterarAtividade'),
    path('sessao/<int:id>',views.inserirsessao,name='inserirSessao'),
    path('eliminaratividade/<id>',views.eliminarAtividade,name='eliminarAtividade'),
    path('eliminarsessao/<id>',views.eliminarSessao,name='eliminarSessao'),
    path('proporatividade',views.proporatividade,name='proporAtividade'),
    path('validaratividade/<int:id>/<int:action>',views.validaratividade,name='validarAtividade'),
    url(r'^veredificios/$',views.veredificios,name="verEdificios"),
    url(r'^versalas/$',views.versalas,name="verSalas"),
    url(r'^verhorarios/$',views.verhorarios,name="verHorarios"),
    url(r'^ajaxaddsessaorow/$',views.sessaoRow,name="ajaxAddSessaoRow"),
]

