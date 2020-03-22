from django.urls import path
from . import views
app_name='atividades'

urlpatterns = [
    path("minhasatividades",views.minhasatividades,name="minhasAtividades"),
    path("proporatividade",views.proporatividade,name="proporAtividade"),
]
