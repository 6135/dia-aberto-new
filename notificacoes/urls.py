from . import views
from django.urls import path
from django.urls import re_path as pattern


app_name = 'notificacoes'

urlpatterns = [
    path('enviar', views.EnviarNotificacao, name="enviar-notificacao"),
    path('<int:pk>/', views.DetalhesNotificacao,
         name="detalhes-notificacao"),

    path('detalhes/<int:id>', views.sem_notificacoes,
         name='sem-notificacoes'),
    path('detalhes/<int:id>/<int:nr>', views.categorias_notificacao_automatica,
         name='categorias-notificacao-automatica'),
    path('apagarnotificacao/<int:id>/<int:nr>', views.apagar_notificacao_automatica,
         name='apagar-notificacao-automatica'),

    path('limpar/<int:id>', views.limpar_notificacoes,
         name='limpar-notificacoes'),
    path('marcarcomolida', views.marcar_como_lida,
         name='ler-notificacoes'),
    #     path('notificar_teste/<str:sigla>/<int:id>', views.enviar_notificacao_automatica,
    #          name='notificar'),
]
