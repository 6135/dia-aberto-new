from django.urls import path, include

from . import views

app_name = 'Notificacoes'


urlpatterns = [

    path('enviarnotificacao', views.enviar_notificacao_automatica,name='enviar-notificacao-automatica'),

]       
