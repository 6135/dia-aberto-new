from django.urls import path
from .views import CriarInscricaoIndividual

urlpatterns = [
    path('criarinscricaoindividual', CriarInscricaoIndividual,
         name='criar-inscricao-individual'),
]
