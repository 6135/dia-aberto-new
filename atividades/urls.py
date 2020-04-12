from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url('minhasatividades',views.minhasatividades,name="minhasAtividades"),
    path('alteraratividade/<int:id>',views.alterarAtividade,name='alterarAtividade'),
    path('inserirsessao/<id>',views.inserirsessao,name='inserirSessao'),
    path(r'^alteraratividade/$',views.alterarAtividade,name='alterarAtividade'),
    path('eliminaratividade/<id>',views.eliminarAtividade,name='eliminarAtividade'),
    path('eliminarsessao/<id>',views.eliminarSessao,name='eliminarSessao'),
    path('proporatividade',views.proporatividade,name='proporAtividade'),
]
