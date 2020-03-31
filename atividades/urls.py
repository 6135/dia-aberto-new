from django.urls import path
from . import views

urlpatterns = [
    path("minhasatividades",views.minhasatividades,name="minhasAtividades"),
    path('alteraratividade/<int:id>',views.alterarAtividade,name='alterarAtividade'),
    path('alteraratividade/<id>',views.alterarAtividade,name='alterarAtividade'),
    path('alterarsessao/<id>',views.alterarSessao,name='alterarSessao'),
    path('eliminaratividade/<id>',views.eliminarAtividade,name='eliminarAtividade'),
    path('eliminarsessao/<id>',views.eliminarSessao,name='eliminarSessao'),
    path('inseriratividade', views.inseriratividade, name= "inserirAtividade"),
    path('sessao/<id>',views.inserirsessao,name='inserirSessao2'),
]
