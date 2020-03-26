from django.urls import path
from . import views

urlpatterns = [
    path("minhasatividades",views.minhasatividades,name="minhasAtividades"),
    path("proporatividade",views.proporatividade,name="proporAtividade"),
    path('inseriratividade', views.inseriratividade, name= "inserirAtividade"),
    path('sessao/<id>',views.inserirsessao,name='inserirSessao'),
    path('novasessao/<id>',views.novasessao,name='novaSessao'),
    path('alteraratividade/<id>',views.alterarAtividade,name='alterarAtividade'),

]
