from django.urls import path
from .views import CriarInscricaoIndividual, CriarInscricaoColetiva

urlpatterns = [
    path('criarinscricaoindividual', CriarInscricaoIndividual,
         name='criar-inscricao-individual'),
    path('criarinscricaocoletiva',CriarInscricaoColetiva, name='criar-inscricao-coletiva'),
]
