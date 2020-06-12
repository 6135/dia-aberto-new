from . import views
from django.urls import path
from django.urls import re_path as pattern



app_name = 'notificacoes'

urlpatterns = [
    path('enviar', views.EnviarNotificacao, name="enviar-notificacao"),
    path('<int:pk>/', views.DetalhesNotificacao,
         name="detalhes-notificacao"),

    path('detalhesnotificacao/<int:id>', views.detalhes_notificacao_automatica,
         name='detalhes-notificacao-automatica'),
    path('apagarnotificacao/<int:id>', views.apagar_notificacao_automatica,
         name='apagar-notificacao-automatica'),
    path('notificar/<int:id>', views.enviar_notificacao_mensagem, name='notificar'),

]
