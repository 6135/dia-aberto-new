from django.contrib import admin
from django.urls import path
from .views import atividade, show, edit, update, destroy
urlpatterns = [
    path('atividade', atividade),
    path('show', show),
    path('edit/<int:id>', edit),
    path('update/<int:id>', update),
    path('delete/<int:id>', destroy),
    path("",views.homepage,name="homepage"),
    path("minhasatividades",views.minhasatividades,name="minhasAtividades"),
    path("proporatividade",views.proporatividade,name="proporAtividade"),
]
