from . import views
from django.urls import path

app_name = 'notificacoes'

urlpatterns = [
    path('enviar', views.EnviarNotificacao, name="enviar-notificacao"),
    path('<int:pk>/', views.DetalhesNotificacao,
         name="detalhes-notificacao"),
#     path('enviarnotificacao', views.enviar_notificacao_automatica,
#          name='enviar-notificacao-automatica'),
#     path('detalhesnotificacao/<int:id>', views.detalhes_notificacao_automatica,
#          name='detalhes-notificacao-automatica'),
         
]
