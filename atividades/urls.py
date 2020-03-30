from django.urls import path
from . import views

urlpatterns = [
    path("minhasatividades",views.minhasatividades,name="minhasAtividades"),
    path("proporatividade",views.proporatividade,name="proporAtividade"),
    path('inseriratividade', views.inseriratividade, name= "inserirAtividade"),
    path('sessao/<id>',views.inserirsessao,name='inserirSessao'),

]
