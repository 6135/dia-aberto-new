from django.contrib import admin
from django.urls import path
from .views import atividade, show, edit, update, destroy
urlpatterns = [
    path('atividade', atividade),
    path('show', show),
    path('edit/<int:id>', edit),
    path('update/<int:id>', update),
    path('delete/<int:id>', destroy),
]
